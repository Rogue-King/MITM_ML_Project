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
    def __init__(self, file_path, mac_address_mapping, ip_address_mapping):
        self.file_path = file_path
        self.mac_address_mapping = mac_address_mapping
        self.ip_address_mapping = ip_address_mapping
        self.packets = rdpcap(file_path)

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
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)
    
        mean = torch.tensor([0.0])
        std = torch.tensor([1.0])

        self.wlr1 = torch.nn.Parameter(torch.normal(mean=mean,std=std), requires_grad=True)
        self.wlr2 = torch.nn.Parameter(torch.normal(mean=mean,std=std), requires_grad=True)
        self.blr1 = torch.nn.Parameter(torch.tensor(0.), requires_grad=True)

        self.wpr1 = torch.nn.Parameter(torch.normal(mean=mean,std=std), requires_grad=True)
        self.wpr2 = torch.nn.Parameter(torch.normal(mean=mean,std=std), requires_grad=True)
        self.bpr1 = torch.nn.Parameter(torch.tensor(0.), requires_grad=True)

        self.wp1 = torch.nn.Parameter(torch.normal(mean=mean,std=std), requires_grad=True)
        self.wp2 = torch.nn.Parameter(torch.normal(mean=mean,std=std), requires_grad=True)
        self.bp1 = torch.nn.Parameter(torch.tensor(0.), requires_grad=True)

        self.wo1 = torch.nn.Parameter(torch.normal(mean=mean,std=std), requires_grad=True)
        self.wo2 = torch.nn.Parameter(torch.normal(mean=mean,std=std), requires_grad=True)
        self.bo1 = torch.nn.Parameter(torch.tensor(0.), requires_grad=True)


def ltsm_unit(self, input_value, long_memory, short_memory):
    # long-term memory
    long_remember_percent = torch.sigmoid((short_memory * self.wlr1) + (input_value * self.wlr2) + self.blr1)
    # short-term memory
    potential_remember_percent = torch.sigmoid((short_memory * self.wpr1) + (input_value * self.wpr2) + self.bpr1)

    potential_memory = torch.tanh((short_memory * self.wp1) + (input_value * self.wp2) + self.bp1)

    updated_long_memory = ((long_memory * long_remember_percent) + (potential_remember_percent * potential_memory))
    
    output_percent = toch.sigmoid((short_memory * self.wo1) + (input_value * self.wo2) + self.bo1)

    updated_short_memory = torch.tanh(updated_long_memory) * output_percent

    return ([updated_long_memory, updated_short_memory])

def forward(self, input):
    long_memory = 0
    short_memory = 0

    for i in range(len(input)):
        long_memory, short_memory = self.ltsm_unit(input, long_memory, short_memory)

    return short_memory

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



path_to_best_checkpoint = trainer.checkpoint_callback.best_model_path


trainer = L.Trainer(max_epochs-2000)
trainer.fit(model, train_dataloaders=dataloader, ckpt_path=path_to_best_checkpoint)

class LightningLTSM(L,LightningModule):
    def __init__()