import pandas as pd
import numpy as np
import platform
import os
import argparse
 
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data(input_data):
    current_dir = os.getcwd()
    if input_data == None:
        if(platform.system() == 'Windows'):
            data = pd.read_csv(current_dir + r'\ARP_Data\Labelled_CSV_Large\Melchior_training_arp_data_1.csv')
        else:
            data = pd.read_csv(current_dir + '/ARP_Data/Labelled_CSV_Large/Melchior_training_arp_data_1.csv')
    else:
        data = pd.read_csv(current_dir + input_data)


    labels = data.iloc[:, -1].values
    features = data.iloc[:, :-1].values
    print(labels)
    print(features)
    # Standardize the features
    scaler = StandardScaler()
    features = scaler.fit_transform(features)
    print(features)

    return features, labels

def training(features, labels):

    # Split the data into training, validation, and test sets
    x_train, x_temp, y_train, y_temp = train_test_split(features, labels, test_size=0.3, random_state=42)
    x_val, x_test, y_val, y_test = train_test_split(x_temp, y_temp, test_size=0.5, random_state=42)

    # Reshape the data for LSTM input (assuming a time series sequence)
    # You might need to reshape according to your data structure
    timesteps = 1
    features = x_train.shape[1]
    print(features)
    x_train = x_train.reshape((-1, timesteps, features))
    x_val = x_val.reshape((-1, timesteps, features))
    x_test = x_test.reshape((-1, timesteps, features))

    print(features)
    # Define your LSTM model
    model = Sequential()
    model.add(LSTM(units=50, input_shape=(timesteps, features)))
    model.add(Dense(units=1, activation='relu'))

    # Compile the model
    model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
    #model.compile(optimizer='adam', loss='mse')

    model.summary()
    model.fit(x_train, y_train, epochs=10, validation_data=(x_val, y_val))

    predictions = model.predict(features)

    # Binarizing predictions
    predictions_bin = (predictions > 0.6).astype(int)

    current_dir = os.getcwd()

    with open(current_dir + "predictions_test.txt", 'w') as file:
        for prediction in predictions_bin:
            file.write(f"{prediction}\n")
    print(predictions_bin)



    print("Evaluating on test data")
    results = model.evaluate(x_test, y_test)
    print("test loss, test acc:", results)

    return model
# Define early stopping
# early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

# Train the model with early stopping
# history = model.fit(x_train, y_train, epochs=100, validation_data=(x_val, y_val), callbacks=[early_stopping])

# Step 5: Saving the Model
# Saving the model to a file
def save_model(model):
    current_dir = os.getcwd()
    if (platform.system() == 'Windows'):
        model.save(current_dir + r'\ml_models\lstm_model.keras')
    else:
        model.save(current_dir + '/ml_models/lstm_model.keras')

#run model on test data

# Step 6: Loading the Model
# Loading the model from a file
def new_model_predictions(features,predictions_path):
    current_dir = os.getcwd()
    if (platform.system() == 'Windows'):
        model = keras.models.load_model(current_dir + r'\ml_models\lstm_model.keras')
    else:
        print(current_dir + '/ml_models/lstm_model.keras')
        model = keras.models.load_model(current_dir + '/ml_models/lstm_model.keras')\

    predictions = model.predict(features)

    #make predictions for new data
    # Step 8: Binarizing the Predictions
    # Binarizing predictions
    predictions_bin = (predictions > 0.6).astype(int)

    # Step 9: Saving the Predictions
    current_dir = os.getcwd()

    with open(current_dir + predictions_path, 'w') as file:
        for prediction in predictions_bin:
            file.write(f"{prediction}\n")
    print(predictions_bin)


def main():
    parser = argparse.ArgumentParser(description='Anomaly Detection using LSTM on ARP packets.')
    parser.add_argument('--input', required=True, help='Path to the pcap or pcapng file for training or prediction.')
    parser.add_argument('--output', help='Path to save the predictions.')
    parser.add_argument('--train', action='store_true', help='Train the model if specified.')
    # parser.add_argument('--model_input', help='Path to the pre-trained model for prediction (ignored if --train is set).')

    args = parser.parse_args()

    if args.train:
        if args.output is None:
            output = 'predictions.txt'
        
        features, labels = load_data(None)
        model = training(features, labels)
        save_model(model)
    
    else:
        # if args.model_input is None:
        #     print("Error: --model_input is required when --train is not set.")
        # el
        if args.input is None:
            print("Error: --input is required when --train is not set.")
        else:
            if (args.output is not None):
                predictions_path = args.output 
            else: 
                predictions_path = 'predictions.txt'
            
            features = load_data(args.input)
            new_model_predictions(features, predictions_path)

if __name__ == "__main__":
    main()