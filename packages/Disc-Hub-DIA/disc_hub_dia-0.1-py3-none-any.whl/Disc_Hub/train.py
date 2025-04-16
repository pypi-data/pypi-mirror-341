import copy
import torch
import torch.nn  as nn
import torch.optim  as optim
import numpy as np
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, TensorDataset
from multiprocessing import Pool
from sklearn.model_selection import KFold, train_test_split
from Disc_Hub.models import ResNetModel, MetaModel, DynamicFocalBCE
import torch.multiprocessing  as mp
import xgboost as xgb

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def train_neural_network(model_id, X_train, y_train, X_val, y_val, device=device,modeltype = 'MLP',
                         epochs=500, patience=5, min_delta=0.001):
    # Initialize the model, loss function, and optimizer
    global loss, criterion, model
    if modeltype == 'MLP' or modeltype == 'MLP+Focal':
        model = ResNetModel(input_dim=X_train.shape[1]).to(device)

    if modeltype == 'MLP':
        criterion = nn.BCELoss()
    elif modeltype == 'MLP+Focal':
        criterion = DynamicFocalBCE()

    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Convert training data to PyTorch tensors
    train_dataset = TensorDataset(torch.FloatTensor(X_train).to(device),
                                  torch.FloatTensor(y_train).view(-1, 1).to(device))
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, drop_last=True)

    # Initialize early stopping variables
    best_val_loss = float('inf')
    patience_counter = 0
    best_model = None

    # Convert validation data to PyTorch tensors
    X_val_tensor = torch.FloatTensor(X_val).to(device)
    y_val_tensor = torch.FloatTensor(y_val).view(-1, 1).to(device)

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0

        # Training phase
        for data, target in train_loader:
            optimizer.zero_grad()
            outputs = model(data)

            # Compute dynamic weights
            with torch.no_grad():
                epoch_tensor = torch.tensor(epoch, dtype=torch.float32, device=device)
                phase = epoch_tensor / 10 * 2 * torch.tensor(np.pi, device=device)

                # Sinusoidal weight modulation
                weight_modulation = 1.0 + 0.5 * torch.sin(phase)

                # Normalize weights and prevent division by zero
                sample_weights = weight_modulation / (weight_modulation.mean() + 1e-8)

                # Clamp weights to avoid extreme values
                sample_weights = torch.clamp(sample_weights, 0, 5.0)

            if modeltype == 'MLP':
                loss = criterion(outputs, target)
            elif modeltype == 'MLP+Focal':
                loss = criterion(outputs, target, epoch, sample_weights)

            loss.backward()
            optimizer.step()
            running_loss += loss.item()

            # Validation phase
        model.eval()
        with torch.no_grad():
            val_outputs = model(X_val_tensor)
            if modeltype == 'MLP':
                val_loss = criterion(val_outputs, y_val_tensor).item()
            elif modeltype == 'MLP+Focal':
                val_loss = criterion(val_outputs, y_val_tensor, epoch, sample_weights).item()

        # Early stopping logic
        if val_loss < (best_val_loss - min_delta):
            best_val_loss = val_loss
            patience_counter = 0
            best_model = copy.deepcopy(model.state_dict())  # Save the best model
        else:
            patience_counter += 1

            # Print training information
        if epoch % 3 == 0:
            print(f"Model {model_id + 1}, Epoch {epoch + 1}/{epochs}, "
                  f"Train Loss: {running_loss / len(train_loader):.4f}, "
                  f"Val Loss: {val_loss:.4f}")

        # Trigger early stopping
        if patience_counter >= patience:
            print(f"Early stopping triggered at epoch {epoch + 1}")
            model.load_state_dict(best_model)  # Restore the best model
            break

    model.eval()
    # 修改后的代码段
    with torch.no_grad():
        train_probs, train_features = model(torch.FloatTensor(X_train).to(device), return_features=True)
        val_probs, val_features = model(torch.FloatTensor(X_val).to(device), return_features=True)

        train_features = train_features.cpu().numpy()
        val_features = val_features.cpu().numpy()
        val_probs = val_probs.flatten().cpu().numpy()
        train_probs = train_probs.flatten().cpu().numpy()
    return (
        model_id,
        val_probs,
        model.cpu().state_dict(),
        val_features,
        train_features,
        train_probs
    )

def train_xgboost(model_id, X_train, y_train, X_val, y_val, early_stop_rounds=10, verbose_eval=50):
    print(f"Training XGBoost model {model_id + 1}")

    # 数据转换
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dval = xgb.DMatrix(X_val, label=y_val)
    dtotal = xgb.DMatrix(X_val)

    # 动态参数配置（启用GPU加速）
    params = {
        'max_depth': 6,
        'eta': 0.1,
        'objective': 'binary:logistic',
        'tree_method': 'hist',  # 使用直方图方法
        'device': device,
        'subsample': 1,
        'lambda': 0
    }

    # 训练过程
    model = xgb.train(
        params, dtrain,
        num_boost_round=300,
        early_stopping_rounds=early_stop_rounds,
        evals=[(dtrain, "train"), (dval, "val")],
        verbose_eval=verbose_eval
    )

    # 仅输出概率预测
    train_pred = model.predict(dtrain)
    val_pred = model.predict(dval)

    return model_id, val_pred, model, train_pred

def train_meta_neural_network_focalloss(meta_features_train, y_train, input_dim, device=device, epochs=500,
                                        patience=5, min_delta=0.001,Postprocessed='MLP+Focal'):
    # Split data into training and validation sets
    global criterion, loss
    indices = np.random.permutation(len(meta_features_train))
    split = int(0.8 * len(indices))

    X_train = meta_features_train[indices[:split]]
    y_train_sub = y_train[indices[:split]]
    X_val = meta_features_train[indices[split:]]
    y_val_sub = y_train[indices[split:]]

    # Convert data to PyTorch tensors
    X_train_tensor = torch.FloatTensor(X_train).to(device)
    y_train_tensor = torch.FloatTensor(y_train_sub).view(-1, 1).to(device)
    X_val_tensor = torch.FloatTensor(X_val).to(device)
    y_val_tensor = torch.FloatTensor(y_val_sub).view(-1, 1).to(device)

    # Initialize the model, optimizer, and loss function
    model = MetaModel(input_dim).to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    if Postprocessed == 'MLP+Focal':
        criterion = DynamicFocalBCE()
    elif Postprocessed == 'MLP':
        criterion = nn.BCELoss()

    # Initialize early stopping variables
    best_val_loss = float('inf')
    patience_counter = 0
    best_model = None

    # Training loop
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()

        # Training predictions
        train_preds = model(X_train_tensor)
        if Postprocessed == 'MLP+Focal':
            loss = criterion(train_preds, y_train_tensor, epoch)
        elif Postprocessed == 'MLP':
            loss = criterion(train_preds, y_train_tensor)
        loss.backward()

        # Gradient clipping
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=2.0)
        optimizer.step()

        # Validation phase
        model.eval()
        with torch.no_grad():
            val_preds = model(X_val_tensor)
            if Postprocessed == 'MLP+Focal':
                val_loss = criterion(val_preds, y_val_tensor, epoch)
            elif Postprocessed == 'MLP':
                val_loss = criterion(val_preds, y_val_tensor)

        # Early stopping logic
        if val_loss < (best_val_loss - min_delta):
            best_val_loss = val_loss
            patience_counter = 0
            best_model = copy.deepcopy(model.state_dict())
        else:
            patience_counter += 1

            # Print training information
        if epoch % 5 == 0:
            print(f"Meta Epoch {epoch + 1}/{epochs}, "
                  f"Train Loss: {loss.item():.4f},   "
                  f"Val Loss: {val_loss:.4f}")

        # Trigger early stopping
        if patience_counter >= patience:
            print(f"Meta Model Early stopping at epoch {epoch + 1}")
            model.load_state_dict(best_model)
            break

    torch.cuda.empty_cache()
    return model

def train_meta_xgboost(meta_features_train, y_train, val_size=0.2, early_stop_rounds=20, random_state=42):
    # 分层分割训练集/验证集
    X_train, X_val, y_train_sub, y_val_sub = train_test_split(
        meta_features_train, y_train,
        test_size=val_size,
        stratify=y_train,
        random_state=random_state
    )

    # 数据转换
    dtrain = xgb.DMatrix(X_train, label=y_train_sub, enable_categorical=True)
    dval = xgb.DMatrix(X_val, label=y_val_sub, enable_categorical=True)

    # 动态参数配置
    params = {
        'max_depth': 3,
        'eta': 0.1,
        'objective': 'binary:logistic',
        'eval_metric': ['logloss', 'error'],
        'tree_method': 'hist',  # 直方图算法加速
        'device': 'cuda',  # 指定GPU
        'subsample': 1,  # 防止过拟合
        'lambda': 0,  # L2正则化
        'seed': random_state
    }

    # 带早停的训练过程
    model = xgb.train(
        params,
        dtrain,
        num_boost_round=500,
        evals=[(dtrain, "train"), (dval, "val")],
        early_stopping_rounds=early_stop_rounds,
        verbose_eval=50
    )

    return model

# 集成策略（动态加权平均）
def dynamic_weighting(probs_matrix):
    # 计算模型置信度权重
    confidence_weights = np.std(probs_matrix, axis=0, keepdims=True)

    # 防止除零错误
    confidence_weights = 1 / (confidence_weights + 1e-8)

    # 归一化权重
    return confidence_weights / confidence_weights.sum(axis=1, keepdims=True)

def train_ensemble_model_kfold(df, x_total, y_total, num_nn=5, n_splits=5, random_state=42,
                               modeltype = 'MLP', Postprocessed = 'weighted mean'):
    # Base feature dimension (output of ResNetModel)
    global results
    base_feature_dim = 32

    # Initialize out-of-fold predictions
    oof_predictions = np.zeros((len(x_total), num_nn * base_feature_dim))
    oof_probs = np.zeros((len(x_total), num_nn))
    final_predictions = np.zeros(len(x_total))

    # K-Fold交叉验证
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=random_state)

    for fold, (train_idx, val_idx) in enumerate(kf.split(x_total)):
        print(f"\n=== Processing Fold {fold + 1}/{n_splits} ===")

        x_train, x_val = x_total[train_idx], x_total[val_idx]
        y_train, y_val = y_total[train_idx], y_total[val_idx]

        # Standardize the data
        scaler = StandardScaler()
        x_train_scaled = scaler.fit_transform(x_train)
        x_val_scaled = scaler.transform(x_val)

        fold_features = []

        # 并行训练基学习器
        if modeltype in ['MLP', 'MLP+Focal']:
            with Pool(processes=num_nn) as pool:
                tasks = [(i, x_train_scaled, y_train, x_val_scaled, y_val, device, modeltype)
                     for i in range(num_nn)]
                results = pool.starmap(train_neural_network, tasks)

            for result in results:
                fold_features.append(result[3])

            oof_predictions[val_idx] = np.hstack(fold_features)

            # 收集验证集概率（按模型ID排序）
            results.sort(key=lambda x: x[0])
            for model_id, val_probs, _, _, _, _ in results:
                oof_probs[val_idx, model_id] = val_probs

        elif modeltype == 'single MLP':
            results = []
            for model_id in range(1):
                result = train_neural_network(
                    model_id=model_id,
                    X_train=x_train_scaled,
                    y_train=y_train,
                    X_val=x_val_scaled,
                    y_val=y_val,
                    device=device
                )
                results.append(result)

            results.sort(key=lambda x: x[0])
            for model_id, val_probs, _ in results:
                for j in range(num_nn):
                    oof_probs[val_idx, j] = val_probs

        elif modeltype == 'XGBoost':
            results = [train_xgboost(0, x_train, y_train, x_val, y_val)]

            for model_id, val_probs, _ , _ in results:
                for j in range(num_nn):
                    oof_probs[val_idx, j] = val_probs

    if Postprocessed == 'weighted mean':
        weights = dynamic_weighting(oof_probs)
        final_predictions = np.sum(oof_probs * weights, axis=1)


        # 后处理（带平滑的归一化）
        final_predictions = (final_predictions - np.min(final_predictions)) / \
                            (np.max(final_predictions) - np.min(final_predictions))

        df['ensemble_prob'] = final_predictions

    elif Postprocessed == 'MLP+Focal' or Postprocessed == 'MLP':
    # Adjust input dimension for the meta-model
        meta_model = train_meta_neural_network_focalloss(
            oof_predictions, y_total,
            input_dim=num_nn * base_feature_dim,
            device=device,
            patience=10,
            min_delta=0.001,
            Postprocessed=Postprocessed
        )

        # Generate final predictions
        meta_features_tensor = torch.FloatTensor(oof_predictions).to(device)
        meta_model.eval()
        with torch.no_grad():
            final_predictions = meta_model(meta_features_tensor).flatten().cpu().numpy()

        # Post-processing: Min-max normalization
        final_predictions = (final_predictions - np.min(final_predictions)) / \
                            (np.max(final_predictions) - np.min(final_predictions))


        # Add final predictions to the DataFrame
        df['ensemble_prob'] = final_predictions

    elif Postprocessed == 'XGBoost':
        # 元模型训练
        meta_model = train_meta_xgboost(
            meta_features_train=oof_probs,
            y_train=y_total,
            val_size=0.2,
            early_stop_rounds=20
        )

        # 最终预测生成
        dtest = xgb.DMatrix(oof_probs)

        final_probs = meta_model.predict(dtest)
        print(final_probs)
        # Post-processing: Min-max normalization
        final_predictions = (final_probs - np.min(final_probs)) / \
                            (np.max(final_probs) - np.min(final_probs))

        # Add final predictions to the DataFrame
        df['ensemble_prob'] = final_predictions

    else:
        print("None model")
    return df

def train_ensemble_model_Fully_Supervised(df, x_total, y_total, num_nn=5, val_size=0.2,
                               modeltype = 'MLP', Postprocessed = 'weighted mean'):
    # Base feature dimension (output of ResNetModel)
    global results
    base_feature_dim = 32

    # Initialize out-of-fold predictions
    oof_predictions = np.zeros((len(x_total), num_nn * base_feature_dim))
    oof_probs = np.zeros((len(x_total), num_nn))
    final_predictions = np.zeros(len(x_total))

    # 单次数据划分（训练集+验证集）
    indices = np.random.permutation(len(x_total))
    split = int((1 - val_size) * len(x_total))

    train_idx, val_idx = indices[:split], indices[split:]
    x_train, x_val = x_total[train_idx], x_total[val_idx]
    y_train, y_val = y_total[train_idx], y_total[val_idx]

    # 数据标准化
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_val_scaled = scaler.transform(x_val)

    # 并行训练基学习器
    if modeltype in ['MLP', 'MLP+Focal']:
        with Pool(processes=num_nn) as pool:
            tasks = [(i, x_train_scaled, y_train, x_val_scaled, y_val, device, modeltype)
                 for i in range(num_nn)]
            results = pool.starmap(train_neural_network, tasks)

            val_features = np.hstack([res[3] for res in results])
            train_features = np.hstack([res[4] for res in results])

            oof_predictions[val_idx] = val_features
            oof_predictions[train_idx] = train_features

        #print(oof_predictions)
        # 收集验证集概率（按模型ID排序）
        results.sort(key=lambda x: x[0])
        for model_id, val_probs, _, _, _, train_probs in results:
            oof_probs[val_idx, model_id] = val_probs
            oof_probs[train_idx, model_id] = train_probs

        print(oof_probs)

    elif modeltype == 'single MLP':
        results = []
        for model_id in range(1):
            result = train_neural_network(
                model_id=model_id,
                X_train=x_train_scaled,
                y_train=y_train,
                X_val=x_val_scaled,
                y_val=y_val,
                device=device
            )
            results.append(result)

        results.sort(key=lambda x: x[0])
        for model_id, val_probs, _ in results:
            for j in range(num_nn):
                oof_probs[val_idx, j] = val_probs


    elif modeltype == 'XGBoost':

        results = [train_xgboost(0, x_train, y_train, x_val, y_val)]

        for model_id, val_probs, _, train_probs in results:

            for j in range(num_nn):
                oof_probs[val_idx, j] = val_probs
                oof_probs[train_idx, j] = train_probs

    else:
        print("None")

    if Postprocessed == 'weighted mean':
        weights = dynamic_weighting(oof_probs)
        final_predictions = np.sum(oof_probs * weights, axis=1)

        # 后处理（带平滑的归一化）
        final_predictions = (final_predictions - np.min(final_predictions)) / \
                            (np.max(final_predictions) - np.min(final_predictions))

        df['ensemble_prob'] = final_predictions

    elif modeltype == 'single MLP':
        results = []
        for model_id in range(1):
            result = train_neural_network(
                model_id=model_id,
                X_train=x_train_scaled,
                y_train=y_train,
                X_val=x_val_scaled,
                y_val=y_val,
                device=device
            )
            results.append(result)

        results.sort(key=lambda x: x[0])
        for model_id, val_probs, _ in results:
            for j in range(num_nn):
                oof_probs[val_idx, j] = val_probs

    elif Postprocessed == 'MLP+Focal' or Postprocessed == 'MLP':
    # Adjust input dimension for the meta-model
        meta_model = train_meta_neural_network_focalloss(
            oof_predictions, y_total,
            input_dim=num_nn * base_feature_dim,
            device=device,
            patience=10,
            min_delta=0.001,
            Postprocessed=Postprocessed
        )

        # Generate final predictions
        meta_features_tensor = torch.FloatTensor(oof_predictions).to(device)
        meta_model.eval()
        with torch.no_grad():
            final_predictions = meta_model(meta_features_tensor).flatten().cpu().numpy()

        # Post-processing: Min-max normalization
        final_predictions = (final_predictions - np.min(final_predictions)) / \
                            (np.max(final_predictions) - np.min(final_predictions))

        # Add final predictions to the DataFrame
        df['ensemble_prob'] = final_predictions

    elif Postprocessed == 'XGBoost':
        # 元模型训练
        meta_model = train_meta_xgboost(
            meta_features_train=oof_probs,
            y_train=y_total,
            val_size=0.2,
            early_stop_rounds=20
        )

        # 最终预测生成
        dtest = xgb.DMatrix(oof_probs)
        final_probs = meta_model.predict(dtest)

        # Post-processing: Min-max normalization
        final_predictions = (final_probs - np.min(final_probs)) / \
                            (np.max(final_probs) - np.min(final_probs))

        # Add final predictions to the DataFrame
        df['ensemble_prob'] = final_predictions

    else:
        print("None")
    return df

def train_ensemble_model_Semi_Supervised(df, x_total, y_total, num_nn=5, val_size=0.2, max_iterations=5,
                               modeltype = 'MLP', Postprocessed = 'weighted mean'):
    # 初始化变量
    y_total_copy = y_total.copy()
    all_predictions = []

    for iteration in range(max_iterations):
        print(f"\nStarting Iteration {iteration + 1}/{max_iterations}")
        # Base feature dimension (output of ResNetModel)
        global results
        base_feature_dim = 32

        # Initialize out-of-fold predictions
        oof_predictions = np.zeros((len(x_total), num_nn * base_feature_dim))
        oof_probs = np.zeros((len(x_total), num_nn))
        final_predictions = np.zeros(len(x_total))

        # 单次数据划分（训练集+验证集）
        indices = np.random.permutation(len(x_total))
        split = int((1 - val_size) * len(x_total))

        train_idx, val_idx = indices[:split], indices[split:]
        x_train, x_val = x_total[train_idx], x_total[val_idx]
        y_train, y_val = y_total[train_idx], y_total[val_idx]

        # 数据标准化
        scaler = StandardScaler()
        x_train_scaled = scaler.fit_transform(x_train)
        x_val_scaled = scaler.transform(x_val)

        # 并行训练基学习器
        if modeltype in ['MLP', 'MLP+Focal']:
            with Pool(processes=num_nn) as pool:
                tasks = [(i, x_train_scaled, y_train, x_val_scaled, y_val, device, modeltype)
                     for i in range(num_nn)]
                results = pool.starmap(train_neural_network, tasks)

                val_features = np.hstack([res[3] for res in results])
                train_features = np.hstack([res[4] for res in results])

                oof_predictions[val_idx] = val_features
                oof_predictions[train_idx] = train_features

            #print(oof_predictions)
            # 收集验证集概率（按模型ID排序）
            results.sort(key=lambda x: x[0])
            for model_id, val_probs, _, _, _, train_probs in results:
                oof_probs[val_idx, model_id] = val_probs
                oof_probs[train_idx, model_id] = train_probs

            print(oof_probs)

        elif modeltype == 'single MLP':
            results = []
            for model_id in range(1):
                result = train_neural_network(
                    model_id=model_id,
                    X_train=x_train_scaled,
                    y_train=y_train,
                    X_val=x_val_scaled,
                    y_val=y_val,
                    device=device
                )
                results.append(result)

            results.sort(key=lambda  x: x[0])
            for model_id, val_probs, _ in results:
                for j in range(num_nn):
                    oof_probs[val_idx, j] = val_probs

        elif modeltype == 'XGBoost':
            results = [train_xgboost(0, x_train, y_train, x_val, y_val)]
            for model_id, val_probs, _, train_probs in results:
                for j in range(num_nn):
                    oof_probs[val_idx, j] = val_probs
                    oof_probs[train_idx, j] = train_probs

        else:
            print("None")

        if Postprocessed == 'weighted mean':
            weights = dynamic_weighting(oof_probs)
            final_predictions = np.sum(oof_probs * weights, axis=1)

            # 后处理（带平滑的归一化）
            final_predictions = (final_predictions - np.min(final_predictions)) / \
                                (np.max(final_predictions) - np.min(final_predictions))

            df['ensemble_prob'] = final_predictions

        elif Postprocessed == 'MLP+Focal' or Postprocessed == 'MLP':
        # Adjust input dimension for the meta-model
            meta_model = train_meta_neural_network_focalloss(
                oof_predictions, y_total,
                input_dim=num_nn * base_feature_dim,
                device=device,
                patience=10,
                min_delta=0.001,
                Postprocessed=Postprocessed
            )

            # Generate final predictions
            meta_features_tensor = torch.FloatTensor(oof_predictions).to(device)
            meta_model.eval()
            with torch.no_grad():
                final_predictions = meta_model(meta_features_tensor).flatten().cpu().numpy()

            # Post-processing: Min-max normalization
            final_predictions = (final_predictions - np.min(final_predictions)) / \
                                (np.max(final_predictions) - np.min(final_predictions))

        elif Postprocessed == 'XGBoost':
            # 元模型训练
            meta_model = train_meta_xgboost(
                meta_features_train=oof_probs,
                y_train=y_total,
                val_size=0.2,
                early_stop_rounds=20
            )

            # 最终预测生成
            dtest = xgb.DMatrix(oof_probs)
            final_probs = meta_model.predict(dtest)

            # Post-processing: Min-max normalization
            final_predictions = (final_probs - np.min(final_probs)) / \
                                (np.max(final_probs) - np.min(final_probs))

        else:
            print("None")

        # 存储当前迭代的预测结果
        all_predictions.append(final_predictions.copy())

        # 后处理
        final_predictions = (final_predictions - final_predictions.min()) / (final_predictions.max() - final_predictions.min())

        # 更新标签
        high_confidence_indices = np.where(np.abs(final_predictions - 0.5) > 0.4)[0]  # 预测概率高于0.9或低于0.1

        for idx in high_confidence_indices:
            if y_total_copy[idx] == 0 and final_predictions[idx] >= 0.9:
                y_total_copy[idx] = 1
            elif y_total_copy[idx] == 1 and final_predictions[idx] <= 0.1:
                y_total_copy[idx] = 0

        if iteration == max_iterations - 1:
            df['semi_prob'] = final_predictions

    return df

def train_ensemble(df, methods, modeltype, Postprocessed):
    # Ensure proper execution of multiprocessing
    mp.set_start_method('spawn', force=True)

    # Extract features and labels
    score_columns = [col for col in df.columns if col.startswith("score")]
    score_data = df[score_columns]
    score_matrix = score_data.to_numpy()

    decoy_data = df['decoy']
    decoy = decoy_data.to_numpy()

    # Convert to x and y
    y_total = 1 - decoy
    x_total = score_matrix

    if methods =='k-fold':
        # Call the main training function
        df = train_ensemble_model_kfold(
            df,
            x_total,
            y_total,
            num_nn=5,
            n_splits=5,
            modeltype=modeltype,
            Postprocessed=Postprocessed
        )

    elif methods == 'fully':
        df = train_ensemble_model_Fully_Supervised(
            df,
            x_total,
            y_total,
            num_nn=5,
            modeltype=modeltype,
            Postprocessed=Postprocessed
        )

    elif methods == 'semi':
        df = train_ensemble_model_Semi_Supervised(
            df,
            x_total,
            y_total,
            num_nn=5,
            max_iterations=5,
            modeltype=modeltype,
            Postprocessed=Postprocessed
        )

    return df