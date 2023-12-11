import os
from flask import request, flash, session
from scapy.all import PcapReader, ARP
import csv
from werkzeug.utils import secure_filename

from webapp.controllers.ml_controller import update_csv_with_predictions

ALLOWED_EXTENSIONS = {".pcap", ".PCAP"}

ARP_MAPPINGS = {
    1: "WHO-HAS",
    2: "IS-AT"
}

def file_upload_success():
    if 'pcap-upload' not in request.files:
        flash('Could not find file uploaded')
        return False
        
    pcap_file = request.files.get('pcap-upload')
    
    if pcap_file.filename == '':
        flash('File not found. Please try again')
        return False

    if os.path.splitext(pcap_file.filename)[1] not in ALLOWED_EXTENSIONS:
        flash('File is not a recognized format. Please upload .pcap files only')
        return False
    
    session['pcap_csv_filepath'] = f'webapp/file_uploads/{secure_filename(pcap_file.filename).replace(".pcap", ".csv")}'
    session['processed_pcap_csv_filepath'] = f'webapp/file_uploads/{secure_filename(pcap_file.filename).replace(".pcap", "_process.csv")}'

    create_csvs(pcap_file)

    update_csv_with_predictions()

    flash(f'Uploaded {secure_filename(pcap_file.filename)} successfully')
    
    return True

def create_csvs(file):
    with open(session.get('pcap_csv_filepath'), 'w', newline="\n") as csv_file, open(session.get('processed_pcap_csv_filepath'), 'w', newline="\n") as preprocessed_csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Packet #','Source IP', 'Destination IP', 'Source MAC', 'Destination MAC', 'Payload'])

        preprocess_writer = csv.writer(preprocessed_csv_file)
        preprocess_writer.writerow(['Source IP', 'Destination IP', 'Source MAC', 'Destination MAC', 'Opcode'])

        parse_pcap_file(file, csv_writer, preprocess_writer)

def parse_pcap_file(file, csv_writer, preprocess_writer):
    packet_number = 1;

    for packet in PcapReader(file):
        if (packet.haslayer(ARP)):
            packet_info = [packet_number, packet.psrc, packet.pdst, packet.src, packet.dst, determine_arp_payload(packet)]
            preprocess_packet_info = [convert_ip_to_dec(packet.psrc), convert_ip_to_dec(packet.pdst), convert_mac_to_dec(packet.src), convert_mac_to_dec(packet.dst), packet.op]

            packet_number += 1;
                        
            csv_writer.writerow(packet_info)
            preprocess_writer.writerow(preprocess_packet_info)

def determine_arp_payload(packet):
    operation = ARP_MAPPINGS.get(packet.op)

    if operation == "WHO-HAS":
        return f"{operation} {packet.pdst}? TELL {packet.psrc}"
    
    if operation == "IS-AT":
        return f"{packet.psrc} {operation} {packet.hwsrc}"
    
def convert_ip_to_dec(ip_address):
    octets = ip_address.split('.')

    return (int(octets[0]) << 24) + (int(octets[1]) << 16) + (int(octets[2]) << 8) + int(octets[3])

def convert_mac_to_dec(mac_address):
    octets = mac_address.split(':')

    return (int(octets[0], 16) << 40) + (int(octets[1], 16) << 32) + (int(octets[2], 16) << 24) + (int(octets[3], 16) << 16) + (int(octets[4], 16) << 8) + int(octets[5], 16)
