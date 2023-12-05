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