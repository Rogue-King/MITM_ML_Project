# from sklearn.preprocessing import StandardScaler
# from scapy.all import *
import argparse
import csv
import os
import sys
from scapy.all import rdpcap

def read_pcap(file_name, output_csv):
    packets = rdpcap(file_name)
    
    with open(output_csv, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        for i, packet in enumerate(packets):
            # Access the binary data of the packet
            packet_data = bytes(packet)
            
            # Convert the binary data to a hexadecimal string
            hex_data = packet_data.hex()
            print(hex_data)
            
            # Write the hexadecimal representation to the CSV file
            csv_writer.writerow([hex_data])


def main():
    parser = argparse.ArgumentParser(description="Read a PCAP file and print its packets.")
    parser.add_argument("-f", "--file", help="Path to the PCAP file to read")
    args = parser.parse_args()

    if not args.file:
        parser.print_help()
        sys.exit(1) 
    
    if not os.path.isfile(args.file):
        print("[-] " + args.file + " does not exist.")
        sys.exit(1)

    read_pcap(args.file, 'output.csv')


if __name__ == "__main__":
    main()




# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)
