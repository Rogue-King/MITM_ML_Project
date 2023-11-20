import threading
import time
import datetime
import random
from scapy.all import sniff, AsyncSniffer, ARP, wrpcap

INTERFACES = ['eth0', 'eth1', 'eth2']

def process_packet(packet, interface, pcap_filename):
    if ARP in packet:
        # Process ARP packet and add the label
        print(f"Received ARP packet on {interface} interface:\n{packet.summary()}")
        
        # Add a label of "1" for malicious
        packet[ARP].pdst = packet[ARP].pdst + " (malicious)"

        wrpcap(pcap_filename, packet, append=True)

def sniff_packets(interface, duration):
    start_time = time.time()
    end_time = start_time + duration

    # Create a unique timestamp for each capture session
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    pcap_filename = f"captured_packets_{interface}_{timestamp}.pcap"

    sniffer = AsyncSniffer(iface=interface, prn=lambda pkt: process_packet(pkt, interface, pcap_filename))
    sniffer.start()

    try:
        while time.time() < end_time:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        sniffer.stop_and_wait()

def activate_agents(num_agents):
    threads = []

    for i in range(min(num_agents, len(INTERFACES))):
        interface = INTERFACES[i]
        duration = random.uniform(120, 240)  # Random duration between 2 to 4 minutes
        start_delay = random.uniform(0, 120)  # Random start delay within the first 2 minutes

        # Create a thread for each interface with a random start delay and duration
        thread = threading.Timer(start_delay, sniff_packets, args=(interface, duration))
        threads.append(thread)
        thread.start()

    return threads

def main():
    try:
        num_agents = int(input("Enter the number of agents to activate: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    if num_agents <= 0:
        print("Number of agents must be greater than zero.")
        return

    threads = activate_agents(num_agents)

    try:
        # Keep the main program running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Stop the sniffers when Ctrl+C is pressed
        print("Stopping sniffers...")
        for thread in threads:
            thread.cancel()

if __name__ == "__main__":
    main()
