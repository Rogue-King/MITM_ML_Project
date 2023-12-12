import os
import pandas as pd    

current_dir = os.getcwd()

label_actual = pd.read_csv(current_dir + '/Casper_training_arp_data_min.csv')['Label'].tolist()
tp, fp, fn, tn = 0, 0, 0, 0

predictions_array = pd.read_csv(current_dir + '/Casper_predictions_min.csv')['Label'].tolist()

for i in predictions_array:
    if (predictions_array[i] and label_actual[i] == 1):
        tp += 1
    elif (predictions_array[i] and label_actual[i] == 0):
        fp += 1
    elif (not predictions_array[i] and label_actual[i] == 1):
        fn += 1
    else:
        tn += 1
    i += 1

avg_positive = (tp + fp) / len(predictions_array)
avg_negative = (tn + fn) / len(predictions_array)

print(f'Statistics(Casper): tp: {tp} fp: {fp} fn: {fn} tn: {tn} avg_positive: {avg_positive} avg_negative: {avg_negative}')