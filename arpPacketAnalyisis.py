#write a program to analyze pcap files for arp packets
#and print out the source and destination MAC and IP addresses

import argparse
import os
import sys
import dpkt

def main():
    parseArpHeader()

def parseArpHeader():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="pcap file to analyze")
    args = parser.parse_args()

    if not args.file:
        parser.print_help()
        sys.exit(1)

    if not os.path.isfile(args.file):
        print("[-] " + args.file + " does not exist.")
        sys.exit(1)

    with open(args.file, 'rb') as f: #rb = read binary
        pcap = dpkt.pcap.Reader(f)
        for timestamp, buf in pcap:
            try:
                eth = dpkt.ethernet.Ethernet(buf)
                if eth.type != dpkt.ethernet.ETH_TYPE_ARP:
                    continue
                arp = eth.arp
                print("Source MAC: " + mac_addr(eth.src) + " Source IP: " + ip_addr(arp.spa))
                print("Destination MAC: " + mac_addr(eth.dst) + " Destination IP: " + ip_addr(arp.tpa))
                print("---------------------------------------------------------")
            except Exception as e:
                print(e)
                continue