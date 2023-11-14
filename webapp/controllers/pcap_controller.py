from scapy.all import PcapReader, ARP

ARP_MAPPINGS = {
    1: "WHO-HAS",
    2: "IS-AT"
}

def parse_pcap_file(file):
    packets_list = [('Packet #','Source IP', 'Destination IP', 'Source MAC', 'Destination MAC', 'Payload')]
    packet_number = 1;
    for packet in PcapReader(file):
        if (packet.haslayer(ARP)):
            packet_info = (packet_number, packet.psrc, packet.pdst, packet.src, packet.dst, determine_arp_payload(packet))
            packet_number += 1;
            packets_list.append(packet_info)

    return packets_list


def determine_arp_payload(packet):
    operation = ARP_MAPPINGS.get(packet.op)

    if operation == "WHO-HAS":
        return "{} {}? TELL {}".format( operation, packet.pdst, packet.psrc )
    
    if operation == "IS-AT":
        return "{} {} {}".format( packet.psrc, operation, packet.hwsrc )
    
