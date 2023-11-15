from scapy.all import *

def packet_handler(packet):
    # Process the packet as needed
    print(packet.summary())

# Define the interfaces you want to sniff on
interface1 = "Maria"
interface2 = "Rose"
interface3 = "Sina"

# Specify the file names for saving the pcap files
pcap_file1 = "capture_Maria1.pcap"
pcap_file2 = "capture_Rose2.pcap"
pcap_file3 = "capture_Sina3.pcap"

# Start sniffing on the first interface and save to pcap file
sniff(iface=interface1, prn=packet_handler, store=0, count=10)
wrpcap(pcap_file1, sniffed_packets)

# Start sniffing on the second interface and save to pcap file
sniff(iface=interface2, prn=packet_handler, store=0, count=10)
wrpcap(pcap_file2, sniffed_packets)

# Start sniffing on the third interface and save to pcap file
sniff(iface=interface3, prn=packet_handler, store=0, count=10)
wrpcap(pcap_file3, sniffed_packets)