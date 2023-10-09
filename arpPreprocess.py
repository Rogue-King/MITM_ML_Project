import numpy as np
from scapy.all import *

def extract_features(packet):
    # Extract relevant features from the packet (customize based on your use case)
    features = [packet[IP].src, packet[IP].dst, packet[IP].proto, len(packet)]
    return featuresdef arp_packet_handler(packet):
    if ARP in packet:
        arp_packet = packet[ARP]
        if arp_packet.op == 1:  # ARP Request
            print(f"ARP Request: {arp_packet.psrc} ({arp_packet.hwsrc}) is looking for {arp_packet.pdst}")

# Sniff ARP packets on a specific interface (e.g., "eth0") for a certain number of packets (count) and call arp_packet_handler for each ARP packet.
sniff(iface="eth0", count=10, prn=arp_packet_handler, filter="arp")
