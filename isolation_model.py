import argparse
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
    return ip_address_mapping

# Function to read pcap file and extract ARP features
def read_arp_pcap(file_path, mac_address_mapping, ip_address_mapping):
    packets = rdpcap(file_path)
    features = [extract_arp_features(packet, mac_address_mapping, ip_address_mapping) for packet in packets if extract_arp_features(packet, mac_address_mapping, ip_address_mapping) is not None]
    return np.array(features)

# Function to train the isolation forest model
def train_isolation_forest(features, model_save_path, contamination=0.05):
    model = IsolationForest(contamination=contamination)
    model.fit(features)
    # Save the trained model to a file using joblib
    dump(model, model_save_path)
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

def main():
    parser = argparse.ArgumentParser(description='Anomaly Detection using Isolation Forest on ARP packets.')
    parser.add_argument('--input', required=True, help='Path to the pcap or pcapng file for training or prediction.')
    parser.add_argument('--output', required=True, help='Path to save or load the model.')
    parser.add_argument('--train', action='store_true', help='Train the model if specified.')
    parser.add_argument('--model_input', help='Path to the pre-trained model for prediction (ignored if --train is set).')

    args = parser.parse_args()

    if args.train:
        # Create a mapping of unique MAC addresses to integer values
        mac_address_mapping = create_mac_address_mapping(args.input)
        # Save the MAC address mapping for later use during prediction
        with open('mac_address_mapping.pkl', 'wb') as mapping_file:
            dump(mac_address_mapping, mapping_file)

        # Create a mapping of unique IP addresses to integer values
        ip_address_mapping = create_ip_address_mapping(args.input)
        # Save the IP address mapping for later use during prediction
        with open('ip_address_mapping.pkl', 'wb') as mapping_file:
            dump(ip_address_mapping, mapping_file)

        # Read pcap file and extract ARP features
        arp_features = read_arp_pcap(args.input, mac_address_mapping, ip_address_mapping)
        isolation_forest_model = train_isolation_forest(arp_features, args.output)
        print("Model trained and saved successfully.")
    else:
        if args.model_input is None:
            print("Error: --model_input is required when --train is not set.")
        else:
            # Load the MAC address mapping from the saved file
            with open('mac_address_mapping.pkl', 'rb') as mapping_file:
                mac_address_mapping = load(mapping_file)

            # Load the IP address mapping from the saved file
            with open('ip_address_mapping.pkl', 'rb') as mapping_file:
                ip_address_mapping = load(mapping_file)

            isolation_forest_model = load_isolation_forest(args.model_input)
            arp_features_to_predict = read_arp_pcap(args.input, mac_address_mapping, ip_address_mapping)
            anomalies = predict_anomalies(isolation_forest_model, arp_features_to_predict)
            print("Predicted Anomalies:")
            print(anomalies)

if __name__ == "__main__":
    main()
