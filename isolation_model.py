import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.externals import joblib  # For scikit-learn version 0.22 and earlier
# If you're using scikit-learn version 0.23 or later, use the following import instead:
# from joblib import dump, load
from scapy.all import *

# Function to extract features from ARP packets
def extract_arp_features(packet):
    if ARP in packet:
        arp_packet = packet[ARP]
        # Extract relevant features from the ARP packet
        features = [
            arp_packet.hwsrc,  # Source hardware address
            arp_packet.psrc,   # Source protocol address
            arp_packet.hwdst,  # Destination hardware address
            arp_packet.pdst    # Destination protocol address
            # Add more features as needed
        ]
        return features
    return None

# Function to read pcap file and extract ARP features
def read_arp_pcap(file_path):
    packets = rdpcap(file_path)
    features = [extract_arp_features(packet) for packet in packets if extract_arp_features(packet) is not None]
    return np.array(features)

# Function to train the isolation forest model
def train_isolation_forest(features, model_save_path, contamination=0.05):
    model = IsolationForest(contamination=contamination)
    model.fit(features)
    # Save the trained model to a file using joblib
    joblib.dump(model, model_save_path)
    return model

# Function to load a pre-trained isolation forest model
def load_isolation_forest(model_load_path):
    # Load the trained model from a file using joblib
    model = joblib.load(model_load_path)
    return model

# Function to predict anomalies using the trained model
def predict_anomalies(model, features):
    predictions = model.predict(features)
    return predictions

# Main function
def main():
    # Path to the pcap file
    pcap_file_path = 'path/to/your/file.pcap'
    
    # Path to save or load the model
    model_save_path = 'path/to/save/model.joblib'
    model_load_path = 'path/to/load/model.joblib'

    # Training or loading the isolation forest model
    train_model = False  # Set to True if you want to train the model, False to load a pre-trained model

    if train_model:
        # Read pcap file and extract ARP features
        arp_features = read_arp_pcap(pcap_file_path)

        # Train the isolation forest model
        isolation_forest_model = train_isolation_forest(arp_features, model_save_path)
    else:
        # Load a pre-trained isolation forest model
        isolation_forest_model = load_isolation_forest(model_load_path)

    # Read pcap file again for prediction
    arp_features_to_predict = read_arp_pcap(pcap_file_path)

    # Predict anomalies
    anomalies = predict_anomalies(isolation_forest_model, arp_features_to_predict)

    # Print the predicted anomalies
    print("Predicted Anomalies:")
    print(anomalies)

if __name__ == "__main__":
    main()
