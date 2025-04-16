import torch
import torch.nn  as nn

class ResNetModel(nn.Module):
    def __init__(self, input_dim):
        super(ResNetModel, self).__init__()
        self.dense1 = nn.Linear(input_dim, 256)
        self.batch_norm1 = nn.BatchNorm1d(256)
        self.dropout1 = nn.Dropout(0.7)

        self.dense2 = nn.Linear(256, 256)
        self.batch_norm2 = nn.BatchNorm1d(256)
        self.dropout2 = nn.Dropout(0.7)

        self.dense3 = nn.Linear(256, 128)
        self.batch_norm3 = nn.BatchNorm1d(128)
        self.dropout3 = nn.Dropout(0.55)

        self.dense4 = nn.Linear(128, 64)
        self.batch_norm4 = nn.BatchNorm1d(64)
        self.dropout4 = nn.Dropout(0.45)

        self.dense5 = nn.Linear(64, 32)
        self.batch_norm5 = nn.BatchNorm1d(32)

        self.output = nn.Linear(32, 1)

    def forward(self, x, return_features=False):
        # Forward pass with residual connection
        x = torch.relu(self.batch_norm1(self.dense1(x)))
        x = self.dropout1(x)

        residual = torch.relu(self.batch_norm2(self.dense2(x)))
        residual = self.dropout2(residual)

        x = torch.add(x, residual)
        x = torch.relu(self.batch_norm3(self.dense3(x)))
        x = self.dropout3(x)

        x = torch.relu(self.batch_norm4(self.dense4(x)))
        x = self.dropout4(x)

        x = torch.relu(self.batch_norm5(self.dense5(x)))
        features = x
        out = torch.sigmoid(self.output(x))

        return (out, features) if return_features else out

class MetaModel(nn.Module):
    def __init__(self, input_dim):
        super(MetaModel, self).__init__()
        self.dense1 = nn.Linear(input_dim, 64)
        self.batch_norm1 = nn.BatchNorm1d(64)
        self.dropout1 = nn.Dropout(0.6)

        self.dense2 = nn.Linear(64, 128)
        self.batch_norm2 = nn.BatchNorm1d(128)
        self.dropout2 = nn.Dropout(0)

        self.dense3 = nn.Linear(128, 64)
        self.batch_norm3 = nn.BatchNorm1d(64)

        self.dense4 = nn.Linear(64, 32)
        self.batch_norm4 = nn.BatchNorm1d(32)

        self.output = nn.Linear(32, 1)

    def forward(self, x):
        # Forward pass for the meta model
        x = torch.relu(self.batch_norm1(self.dense1(x)))
        x = self.dropout1(x)

        x = torch.relu(self.batch_norm2(self.dense2(x)))
        x = self.dropout2(x)

        x = torch.relu(self.batch_norm3(self.dense3(x)))

        x = torch.relu(self.batch_norm4(self.dense4(x)))

        out = torch.sigmoid(self.output(x))  # Output probability
        return out


class DynamicFocalBCE(nn.Module):
    def __init__(self, alpha=0.25, gamma=2.0, smooth=1e-6):
        super().__init__()
        self.alpha = alpha
        self.base_gamma = gamma
        self.smooth = smooth
        self.gamma_scheduler = lambda e: 2.0 + 2 * (e / 200)

    def forward(self, inputs, targets, epoch):
        # Dynamic Focal Loss calculation
        current_gamma = self.gamma_scheduler(epoch)
        bce_loss = nn.functional.binary_cross_entropy(inputs, targets, reduction='none')
        pt = torch.exp(-bce_loss)
        focal_factor = self.alpha * (1 - pt) ** current_gamma
        loss = focal_factor * bce_loss  # Core formula of DynamicFocalBCE
        return loss.mean()