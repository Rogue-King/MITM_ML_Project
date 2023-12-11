from scapy.all import PcapReader, ARP
import os
import csv

'''
Attack MAC Address Mappings:
    'Melchior': 'A6:85:95:1E:A3:1C',
    'Balthasar': '52:AC:C2:47:F9:B5',
    'Casper': '6A:76:E5:4C:3E:45'
'''


ATTACKERS_MAC_ADDRESS = ['a6:85:95:1e:a3:1c','52:ac:c2:47:f9:b5','6a:76:e5:4c:3e:45']
TARGET_IP_ADDRESS = ['10.21.0.16', '10.21.0.17', '10.21.0.18']
ROUTER_IP = "10.21.0.5" 

ARP_MAPPINGS = {
    1: "WHO-HAS",
    2: "IS-AT"
}

def main():
    for file in os.listdir('PCAP'):
        pcap_filepath = os.path.join('PCAP', file)
        if (pcap_filepath.endswith('.pcap')):
                create_csv(pcap_filepath, file)


def create_csv(pcap_filepath, filename):
    filename = filename.replace('.pcap', '.csv')
    unlabeled_data_file_path = f'UL_CSV/{filename}'
    labeled_data_file_path = f'L_CSV/{filename}'


    with open(unlabeled_data_file_path, 'w', newline="\n") as UL_csv_file, open(labeled_data_file_path, 'w', newline="\n") as L_csv_file:
        UL_csv_writer = csv.writer(UL_csv_file)
        L_csv_writer = csv.writer(L_csv_file)

        UL_csv_writer.writerow(['Source IP', 'Destination IP', 'Source MAC', 'Destination MAC', 'Opcode'])
        
        L_csv_writer.writerow(['Source IP', 'Destination IP', 'Source MAC', 'Destination MAC', 'Opcode', 'Label'])


        parse_pcap_file(pcap_filepath, UL_csv_writer, L_csv_writer)

def parse_pcap_file(pcap_filepath, UL_csv_writer, L_csv_writer):
    # packet_number = 1;

    for packet in PcapReader(pcap_filepath):
        if (packet.haslayer(ARP)):
            # Unlabeled Data
            packet_info = [convert_ip_to_dec(packet.psrc), convert_ip_to_dec(packet.pdst), convert_mac_to_dec(packet.src), convert_mac_to_dec(packet.dst), packet.op]
            UL_csv_writer.writerow(packet_info)

            # Labeled Data
            is_attack_packet = (packet.hwsrc in ATTACKERS_MAC_ADDRESS and (packet.psrc in TARGET_IP_ADDRESS or packet.psrc == ROUTER_IP))
            label = 1 if is_attack_packet else 0
            
            packet_info.append(label) 
            L_csv_writer.writerow(packet_info)
            
            # packet_number += 1

def convert_ip_to_dec(ip_address):
    octets = ip_address.split('.')

    return (int(octets[0]) << 24) + (int(octets[1]) << 16) + (int(octets[2]) << 8) + int(octets[3])

def convert_mac_to_dec(mac_address):
    octets = mac_address.split(':')

    return (int(octets[0], 16) << 40) + (int(octets[1], 16) << 32) + (int(octets[2], 16) << 24) + (int(octets[3], 16) << 16) + (int(octets[4], 16) << 8) + int(octets[5], 16)

def determine_arp_payload(packet):
    operation = ARP_MAPPINGS.get(packet.op)

    if operation == "WHO-HAS":
        return f"{operation} {packet.pdst}? TELL {packet.psrc}"
    
    if operation == "IS-AT":
        return f"{packet.psrc} {operation} {packet.hwsrc}"
    
if __name__ == "__main__":
    main()