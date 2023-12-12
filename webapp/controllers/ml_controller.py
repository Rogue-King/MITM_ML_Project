import torch
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from flask import session

from webapp.models.LSTM_model import LSTMNN

def init_model():
    model = LSTMNN()
    device = torch.device('cpu')
    model.load_state_dict(torch.load('webapp/models/LSTM_model.pt', map_location=device))
    model.eval()

    return model

def update_csv_with_predictions():
    model = init_model()

    scaler = StandardScaler()
    
    data = pd.read_csv(session.get('processed_pcap_csv_filepath')).values
    data_scaled = scaler.fit_transform(data)

    with torch.no_grad():
        predictions = model(torch.tensor(data_scaled)).numpy()
    
    predictions_bin = (predictions > 0.6).astype(int).tolist()
    predictions_array = [i[0] for i in predictions_bin]

    packet_table_csv = pd.read_csv(session.get('pcap_csv_filepath'))
    packet_table_csv['Label'] = pd.Series(predictions_array, index=packet_table_csv.index)

    packet_table_csv.to_csv(session.get('pcap_csv_filepath'), index=False)

    current_dir = os.getcwd()
    #new_directory = os.path.abspath(os.path.join(current_dir, '..', '..'))
    # print(new_directory + '/Scripts/Data_Label_Script/L_CSV/Melchior_training_arp_data_min.csv')
    label_actual = pd.read_csv(current_dir + '/Scripts/Data_Label_Script/L_CSV/Melchior_training_arp_data_min.csv')['Label'].tolist()
    tp, fp, fn, tn = 0, 0, 0, 0,
    for i in predictions_array:
        if (predictions_array[i] and label_actual[i] == 1):
            tp += 1
        elif (predictions_array[i] and label_actual[i] == 0):
            fp += 1
        elif (not predictions_array[i] and label_actual[i] == 1):
            fn += 1
        else:
            print(predictions_array) 
            print(label_actual)
            tn += 1
        i += 1

    print(f'Statistics: tp: {tp} fp: {fp} fn: {fn} tn: {tn}')