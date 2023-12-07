import argparse
import time
import numpy as np
from sklearn.ensemble import IsolationForest
from joblib import dump, load
from scapy.all import *

# Function to extract features from ARP packets
def extract_arp_features(packet, mac_address_mapping, ip_address_mapping):
    if ARP in packet:
        arp_packet = packet[ARP]
        # Extract relevant features from the ARP packet
        src_mac = arp_packet.hwsrc
        dst_mac = arp_packet.hwdst
        src_ip = arp_packet.psrc
        dst_ip = arp_packet.pdst

        # Use the mapping to assign integer values to MAC and IP addresses
        src_mac_value = mac_address_mapping.get(src_mac, -1)
        dst_mac_value = mac_address_mapping.get(dst_mac, -1)
        src_ip_value = ip_address_mapping.get(src_ip, -1)
        dst_ip_value = ip_address_mapping.get(dst_ip, -1)

        features = [
            src_mac_value,   # Source hardware address
            dst_mac_value,   # Destination hardware address
            src_ip_value,    # Source protocol address
            dst_ip_value     # Destination protocol address
            # Add more features as needed
        ]
        return features
    return None

# Function to create a mapping of unique MAC addresses to integer values
def create_mac_address_mapping(file_path):
    packets = rdpcap(file_path)
    unique_macs = set()

    for packet in packets:
        if ARP in packet:
            arp_packet = packet[ARP]
            unique_macs.add(arp_packet.hwsrc)
            unique_macs.add(arp_packet.hwdst)

    # Create a mapping of unique MAC addresses to integer values
    mac_address_mapping = {mac: i for i, mac in enumerate(unique_macs)}
    print(mac_address_mapping)
    return mac_address_mapping

# Function to create a mapping of unique IP addresses to integer values
def create_ip_address_mapping(file_path):
    packets = rdpcap(file_path)
    unique_ips = set()

    for packet in packets:
        if ARP in packet:
            arp_packet = packet[ARP]
            unique_ips.add(arp_packet.psrc)
            unique_ips.add(arp_packet.pdst)

    # Create a mapping of unique IP addresses to integer values
    ip_address_mapping = {ip: i for i, ip in enumerate(unique_ips)}
    print(ip_address_mapping)
    return ip_address_mapping

# Function to read pcap file and extract ARP features
def read_arp_pcap(file_path, mac_address_mapping, ip_address_mapping):
    start = time.time()
    packets = rdpcap(file_path)
    features = [extract_arp_features(packet, mac_address_mapping, ip_address_mapping) for packet in packets if extract_arp_features(packet, mac_address_mapping, ip_address_mapping) is not None]
    end_time = time.time()

    # Calculate the time taken to read the pcap file
    read_time = end_time - start
    print("Read and Process the pcap file time: {:.2f} seconds".format(read_time))

    return np.array(features)

# Function to train the isolation forest model
def train_isolation_forest(features, model_name, contamination=0.05):
    start_time = time.time()  # Record the start time
    model = IsolationForest(contamination=contamination)
    model.fit(features)
    end_time = time.time()  # Record the end time

    # Calculate the training time
    training_time = end_time - start_time
    print("Model training time: {:.2f} seconds".format(training_time))

    # Save the trained model to a file using joblib
    if model_name.endswith('.joblib'):
        model_output_path = model_name
    else:
        model_output_path = model_name + '.joblib' 
    dump(model, model_output_path)
    return model

# Function to load a pre-trained isolation forest model
def load_isolation_forest(model_load_path):
    # Load the trained model from a file using joblib
    model = load(model_load_path)
    return model

# Function to predict anomalies using the trained model
def predict_anomalies(model, features):
    predictions = model.predict(features)
    return predictions

def save_predictions(predictions, output):
    with open(output, 'w') as file:
        for prediction in predictions:
            file.write(f"{prediction}\n")

def main():
    parser = argparse.ArgumentParser(description='Anomaly Detection using Isolation Forest on ARP packets.')
    parser.add_argument('--input', required=True, help='Path to the pcap or pcapng file for training or prediction.')
    parser.add_argument('--output', help='Path to save the predictions.')
    parser.add_argument('--train', action='store_true', help='Train the model if specified.')
    parser.add_argument('--model_input', help='Path to the pre-trained model for prediction (ignored if --train is set).')
    parser.add_argument('--model_output', help='Path to save or load the model.')
    #parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')

    args = parser.parse_args()

    if args.train:
        if args.model_output is None:
            print("Error: --model_output is required when --train is set.")
        elif args.output is None:
            output = 'predictions.txt'


        # Create a mapping of unique MAC addresses to integer values
        mac_address_mapping = create_mac_address_mapping(args.input)

        # Create a mapping of unique IP addresses to integer values
        ip_address_mapping = create_ip_address_mapping(args.input)

        # Read pcap file and extract ARP features
        arp_features = read_arp_pcap(args.input, mac_address_mapping, ip_address_mapping)
        isolation_forest_model = train_isolation_forest(arp_features, args.model_output)

        print("Model trained and saved successfully.")

        # load model
        # Create a mapping of unique MAC addresses to integer values
        mac_address_mapping = create_mac_address_mapping(args.input)

        # Create a mapping of unique IP addresses to integer values
        ip_address_mapping = create_ip_address_mapping(args.input)

        isolation_forest_model = load_isolation_forest(args.model_output)
        arp_features_to_predict = read_arp_pcap(args.input, mac_address_mapping, ip_address_mapping)
        anomalies = predict_anomalies(isolation_forest_model, arp_features_to_predict)
        save_predictions(anomalies, output)
        print ("Predictions saved to file: {}".format(output))
        print("Predicted Anomalies:")
        print(anomalies)

    else:
        if args.model_input is None:
            print("Error: --model_input is required when --train is not set.")
        else:

            # Load the model and mappings during prediction
            # Create a mapping of unique MAC addresses to integer values
            mac_address_mapping = create_mac_address_mapping(args.input)

            # Create a mapping of unique IP addresses to integer values
            ip_address_mapping = create_ip_address_mapping(args.input)
            
            isolation_forest_model, mac_address_mapping, ip_address_mapping = load_isolation_forest(args.model_input)
            arp_features_to_predict = read_arp_pcap(args.input, mac_address_mapping, ip_address_mapping)
            anomalies = predict_anomalies(isolation_forest_model, arp_features_to_predict)
            print("Predicted Anomalies:")
            print(anomalies)

if __name__ == "__main__":
    main()