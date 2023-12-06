import numpy as np
from scapy.all import *

def arp_packet_handler(packet):
    if ARP in packet:
        arp_packet = packet[ARP]
        if arp_packet.op == 1:  # ARP Request
            print(f"ARP Request: {arp_packet.psrc} ({arp_packet.hwsrc}) is looking for {arp_packet.pdst}")

# Sniff ARP packets on a specific interface (e.g., "eth0") for a certain number of packets (count) and call arp_packet_handler for each ARP packet.
sniff(iface="eth0", count=10, prn=arp_packet_handler, filter="arp")

def extract_features_from_packet(packet):
    # Extract features from a packet
    # This is a simplistic example, modify it based on your requirements
    src_ip = packet[IP].src if IP in packet else '0.0.0.0'
    dst_ip = packet[IP].dst if IP in packet else '0.0.0.0'
    protocol = packet[IP].proto if IP in packet else 0
    length = len(packet)
    
    return [src_ip, dst_ip, protocol, length]

def process_pcap_file(file_path):
    # Read the pcap file
    packets = rdpcap(file_path)

    # Extract features from each packet
    features = [extract_features_from_packet(packet) for packet in packets]

    return np.array(features)

# Example usage
pcap_file_path = 'example.pcap'
X = process_pcap_file(pcap_file_path)

# Now X contains the extracted features from the pcap file
# You might need to further preprocess or transform X based on your requirements

# Assuming you have a function to extract labels from your dataset
def extract_labels_from_pcap(file_path):
    # Implement your label extraction logic here
    # This is a simplistic example, modify it based on your requirements
    labels = []

    # For example, label all traffic as 1 (malicious) for demonstration purposes
    for _ in range(len(rdpcap(file_path))):
        labels.append(1)

    return np.array(labels)

# Example usage
pcap_file_path = 'example.pcap'
y = extract_labels_from_pcap(pcap_file_path)

# Now y contains the labels corresponding to the extracted features (X)
