import torch
import torch.nn as nn

class CVAE(nn.Module):
    def __init__(self, input_dim, condition_dim, latent_dim):
        super(CVAE, self).__init__()

        self.fc1 = nn.Linear(input_dim + condition_dim, 128)
        self.bn1 = nn.BatchNorm1d(128)
        self.fc2 = nn.Linear(128, 64)
        self.bn2 = nn.BatchNorm1d(64)
        self.fc2_5 = nn.Linear(64, 32)
        self.bn2_5 = nn.BatchNorm1d(32)
        self.fc_mu = nn.Linear(32, latent_dim)
        self.fc_logvar = nn.Linear(32, latent_dim)


        self.fc3 = nn.Linear(latent_dim + condition_dim, 64)
        self.bn3 = nn.BatchNorm1d(64)
        self.fc3_5 = nn.Linear(64, 32)
        self.bn3_5 = nn.BatchNorm1d(32)
        self.fc4 = nn.Linear(32, 128)
        self.bn4 = nn.BatchNorm1d(128)
        self.fc5 = nn.Linear(128, input_dim)

        self.dropout = nn.Dropout(p=0.3)

    def encode(self, x, condition):
        x = torch.cat([x, condition], dim=1)
        h = self.dropout(nn.functional.relu(self.bn1(self.fc1(x))))
        h = self.dropout(nn.functional.relu(self.bn2(self.fc2(h))))
        h = self.dropout(nn.functional.relu(self.bn2_5(self.fc2_5(h))))
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)
        return mu, logvar

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z, condition):
        z = torch.cat([z, condition], dim=1)
        h = self.dropout(nn.functional.relu(self.bn3(self.fc3(z))))
        h = self.dropout(nn.functional.relu(self.bn3_5(self.fc3_5(h))))
        h = self.dropout(nn.functional.relu(self.bn4(self.fc4(h))))
        return self.fc5(h)

    def forward(self, x, condition):
        mu, logvar = self.encode(x, condition)
        z = self.reparameterize(mu, logvar)
        return self.decode(z, condition), mu, logvar
