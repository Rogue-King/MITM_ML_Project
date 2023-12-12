#https://github.com/netrialiarahmi/LSTM-Pytorch-Lightning/blob/main/LSTM-Pytorch-Lightning.py
#https://github.com/D-dot-AT/Stock-Prediction-Neural-Network-and-Machine-Learning-Examples/blob/main/common.py

import pandas as pd
import pytorch_lightning as L
import argparse
import torch
import os
from sklearn.metrics import precision_score, accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


from common import print_statistics

# Step 1: Data Preparation
# Loading the training data
current_dir = os.getcwd()

train_data = pd.read_csv(current_dir + '/Melchior_training_arp_data_1_sequence.csv', header=None)
X = train_data.iloc[:, :-1].values
Y = train_data.iloc[:, -1].values

# Scaling the feature data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 2: Model Creation
# Determining the number of input features
input_features = X_scaled.shape[1]

# Creating the LSTM neural network model
class LSTMNN(L.LightningModule):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(input_size=input_features, hidden_size=64, batch_first=True)
        self.fc = nn.Linear(64, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = x.type(self.lstm.weight_ih_l0.dtype)
        x = x.view(-1, 1, input_features)  # Reshaping to match the LSTM input shape
        h_0, _ = self.lstm(x)
        h_0 = h_0[:, -1, :]
        x = self.sigmoid(self.fc(h_0))
        return x

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = nn.BCELoss()(y_hat, y.view(-1, 1).float())
        self.log('train_loss', loss)

        # output_i = self.foward(x[0])
        # loss = (output_i - y)**2
        # self.log('train_loss', loss)
        # if (y == 0):
        #     self.log('out_0', loss)
        # else: 
        #     self.log('out_1', loss)

        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.001)

# Initializing the LSTM model
model = LSTMNN()

# Step 3: Training the Model
# Preparing data loaders
train_dataset = TensorDataset(torch.tensor(X_scaled), torch.tensor(Y))
train_loader = DataLoader(train_dataset, batch_size=32)

# trainer = L.Trainer(default_root_dir=current_dir + '/ml_models/LSTM_model.ckpt')
trainer = L.Trainer(max_epochs=10)
# Initializing a trainer and training the model
# best_model_path = 'lightning_logs/version_0/checkpoints/epoch=9-step=4350.ckpt'
# # print(best_model_path)


# path_to_best_checkpoint = trainer.checkpoint_callback.best_model_path

trainer.fit(model, train_loader)



# Step 4: Testing the Model
# Loading the test data
test_data = pd.read_csv(current_dir + '/Balthasar_training_arp_data_min_sequence.csv', header=None)
X_test = test_data.iloc[:, :-1].values
Y_test = test_data.iloc[:, -1].values

# Scaling the test data
X_test_scaled = scaler.transform(X_test)

# Making predictions
model.eval()
with torch.no_grad():
    predictions = model(torch.tensor(X_test_scaled)).numpy()


# Binarizing predictions
predictions_bin = (predictions > 0.6).astype(int)

current_dir = os.getcwd()

with open(current_dir + '/predictions.txt', 'w') as file:
    for prediction in predictions_bin:
        file.write(f"{prediction}\n")

# Calculating metrics
precision = precision_score(Y_test, predictions_bin)
accuracy = accuracy_score(Y_test, predictions_bin)
TN, FP, FN, TP = confusion_matrix(Y_test, predictions_bin).ravel()

print_statistics(tp=TP, fp=FP, tn=TN, fn=FN)

#save model
torch.save(model.state_dict(), current_dir + '/ml_models/LSTM_model.pt')

