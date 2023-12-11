import torch
import pytorch_lightning as L
from torch import nn 

class LSTMNN(L.LightningModule):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(input_size=5, hidden_size=64, batch_first=True)
        self.fc = nn.Linear(64, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = x.type(self.lstm.weight_ih_l0.dtype)
        x = x.view(-1, 1, 5)
        h_0, _ = self.lstm(x)
        h_0 = h_0[:, -1, :]
        x = self.sigmoid(self.fc(h_0))
        return x

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = nn.BCELoss()(y_hat, y.view(-1, 1).float())
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.001)