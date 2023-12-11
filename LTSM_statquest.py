import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam

import lightning as L
from torch.utils.data import TensorDataset, DataLoader

import numpy as np
import pandas as pd



# Define the dataset class

class ARPDataset(Dataset):
    def __init__(self, file_path):
        self.file_path = pd.readcsv(file_path)

    def __len__(self):
        return len(self.packets)

    def __getitem__(self, idx):
        packet = self.packets[idx]
        features = extract_arp_features(packet, self.mac_address_mapping, self.ip_address_mapping)
        return np.array(features)
    
# Define the model
class ARPLSTM(L.LightningModule):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(input_size=6, hidden_size=1)
        # self.linear = nn.Linear(1, 1)
        # self.loss = nn.MSELoss()

    def forward(self, input):
        input_trans = input.view(len(input), 1)

        lstm_out, temp = self.lstm(input_trans)

        prediction = lstm_out[-1]
        return prediction

    def configure_optimizers(self):
        return torch.optim.SGD(self.model.parameters(), lr=0.1)

    def training_step(self, batch, batch_idx):
        input_i, label_i = batch
        output_i = self.foward(input_i[0])
        loss = (output_i - label_i)**2

        self.log('train_loss', loss)

        if(label_i == 0):
            self.log('train_normal_loss', loss)
        else:
            self.log('train_anomaly_loss', loss)
        return loss


model = ARPLSTM()

print("\nNOw let's compare the observed and predicted values...")
print("Observed: ", output_i)

model(torch.tensor([features[0]]).detach())

inputs = torch.tensor(features[0:1000])
labels = torch.tensor(labels[0:1000])

dataset = TensorDataset(inputs, labels)
dataloader = DataLoader(dataset)

trainer = L.Trainer(max_epochs=2000, log_every_n_steps=2)

path_to_best_checkpoint = trainer.checkpoint_callback.best_model_path

trainer.fit(model, train_dataloaders=dataloader, ckpt_path=path_to_best_checkpoint)

def main():
    # Load the dataset
    dataset = ARPDataset("data.csv")

    # Split the dataset into train and test
    train_size = int(0.8 * len(dataset))
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])

    # Create the dataloaders
    train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=1, shuffle=True)
    test_dataloader = torch.utils.data.DataLoader(test_dataset, batch_size=1, shuffle=True)

    # Train the model
    model = ARPLSTM()
    trainer = L.Trainer(max_epochs=2000, log_every_n_steps=2)
    trainer.fit(model, train_dataloaders=train_dataloader)

    # Test the model
    trainer.test(test_dataloaders=test_dataloader)

    # Save the model
    torch.save(model.state_dict(), "model.pt")

    # Load the model
    model = ARPLSTM()
    model.load_state_dict(torch.load("model.pt"))
    model.eval()

    # Predict on a single packet
    packet = dataset[0]
    features = extract_arp_features(packet, mac_address_mapping, ip_address_mapping)
    prediction = model(torch.tensor([features]).detach())
    print("Prediction: ", prediction)

    # Predict on a batch of packets
    batch_size = 10
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
    for batch in dataloader:
        inputs, labels = batch
        predictions = model(inputs.detach())
        print("Predictions: ", predictions)
        print("Labels: ", labels)
        break