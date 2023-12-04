import os
from flask import request, flash, session
from scapy.all import PcapReader, ARP
import csv
from werkzeug.utils import secure_filename


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
    
    session['pcap_filepath'] = f'webapp/file_uploads/{secure_filename(pcap_file.filename).replace(".pcap", ".csv")}'
        
    create_csv(pcap_file)

    flash(f'Uploaded {secure_filename(pcap_file.filename)} successfully')
    
    return True

def create_csv(file):
    with open(session.get('pcap_filepath'), 'w', newline="\n") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Packet #','Source IP', 'Destination IP', 'Source MAC', 'Destination MAC', 'Payload'])

        parse_pcap_file(file, csv_writer)

def parse_pcap_file(file, writer):
    packet_number = 1;

    for packet in PcapReader(file):
        if (packet.haslayer(ARP)):
            packet_info = [packet_number, packet.psrc, packet.pdst, packet.src, packet.dst, determine_arp_payload(packet)]
            packet_number += 1;

            writer.writerow(packet_info)

def determine_arp_payload(packet):
    operation = ARP_MAPPINGS.get(packet.op)

    if operation == "WHO-HAS":
        return f"{operation} {packet.pdst}? TELL {packet.psrc}"
    
    if operation == "IS-AT":
        return f"{packet.psrc} {operation} {packet.hwsrc}"