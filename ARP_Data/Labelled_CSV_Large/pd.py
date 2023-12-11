import pandas as pd
import glob
import os

# List of file names
file_names = ['Melchior_training_arp_data_1.csv', 'Balthasar_training_arp_data_1.csv', 'Casper_training_arp_data_1.csv']

# Get data file names
path = '/mnt/c/Users/migue/Documents/GitHub/MITM_ML_Project/ARP_Data/Labelled_CSV_Large/'
# Initialize an empty DataFrame to store the combined data
combined_data = pd.DataFrame()

# Loop through the list of file names and read each CSV file into a DataFrame
for file_name in file_names:
    df = pd.read_csv(file_names)
    combined_data = combined_data.append(df, ignore_index=True)

# Write the combined DataFrame to a new CSV file
combined_data.to_csv('ARP_Large.csv', index=False)

print("CSV files combined successfully and saved as 'combined_file.csv'.")