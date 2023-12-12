import os


current_dir = os.getcwd()
new_directory = os.path.abspath(os.path.join(current_dir, '..', '..'))
print(f'{new_directory}' + '/scripts/Data_Label_Script/L_CSV/Melchior_training_arp_data_min.csv')