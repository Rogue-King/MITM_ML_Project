from scapy.all import *
import threading
import random
import time

# Define a lock to ensure exclusive access to network interfaces
lock = threading.Lock()

def send_packet(agent, target_ip, message):
    packet = IP(dst=target_ip) / ICMP() / message
    with lock:
        send(packet, iface=agent)

def agent_listener(agent, target_ip, pcap_file, sniff_active):
    while True:
        if sniff_active.is_set():
            sniff(iface=agent, prn=lambda x: handle_packet(x, target_ip, pcap_file))

def handle_packet(packet, target_ip, pcap_file):
    if (IP in packet and (packet[IP].dst == target_ip or packet[IP].src == target_ip) and ICMP in packet) or (ARP in packet and packet[ARP].psrc == target_ip):
        print(f"Received message from {packet[IP].src}: {packet[ICMP].load.decode()} - Marked as malicious (1)")
        
        # Add a custom field to mark the packet as malicious
        if ICMP in packet:
            packet[ICMP].malicious = 1
        elif ARP in packet:
            packet[ARP].malicious = 1
        
        with lock:
            wrpcap(pcap_file, packet, append=True)

def agent_sender(agent_interface, target_ip, message):
    with lock:
        send_packet(agent_interface, target_ip, message)

def choose_random_target(current_target, all_targets):
    available_targets = list(set(all_targets) - {current_target})
    return random.choice(available_targets)

def communicate_with_random_target(agent_interface, target_ip):
    duration = random.uniform(120, 240)  # Random communication duration between 2 and 4 minutes
    print(f"{agent_interface} communicating with {target_ip} for {duration} seconds.")
    
    start_time = time.time()
    while time.time() - start_time < duration:
        time.sleep(1)  # Simulate communication
        message = f"Random message to {target_ip}!"
        agent_sender(agent_interface, target_ip, message)

if __name__ == "__main__":
    agent1_interface = "your_network_interface1"  # Replace with the actual network interface
    agent2_interface = "your_network_interface2"  # Replace with the actual network interface
    agent3_interface = "your_network_interface3"  # Replace with the actual network interface

    target_ip_agent = ["10.21.0.16", "10.21.0.17", "10.21.0.18"]

    pcap_file_agent1 = "agent1_traffic.pcap"
    pcap_file_agent2 = "agent2_traffic.pcap"
    pcap_file_agent3 = "agent3_traffic.pcap"

    sniff_active_agent1 = threading.Event()
    sniff_active_agent2 = threading.Event()
    sniff_active_agent3 = threading.Event()

    agent_listener_thread1 = threading.Thread(target=agent_listener, args=(agent1_interface, target_ip_agent[0], pcap_file_agent1, sniff_active_agent1))
    agent_listener_thread2 = threading.Thread(target=agent_listener, args=(agent2_interface, target_ip_agent[0], pcap_file_agent2, sniff_active_agent2))
    agent_listener_thread3 = threading.Thread(target=agent_listener, args=(agent3_interface, target_ip_agent[0], pcap_file_agent3, sniff_active_agent3))

    agent_listener_thread1.start()
    agent_listener_thread2.start()
    agent_listener_thread3.start()

    # Simulate communication for random durations
    for i in range(5):  # Communicate 5 times as an example
        time.sleep(1)  # Introduce a delay between communications

        # Activate the sniffer for the agents during communication
        sniff_active_agent1.set()
        sniff_active_agent2.set()
        sniff_active_agent3.set()

        random_target_agent1 = choose_random_target(target_ip_agent[0], target_ip_agent)
        random_target_agent2 = choose_random_target(target_ip_agent[0], target_ip_agent)
        random_target_agent3 = choose_random_target(target_ip_agent[0], target_ip_agent)

        communicate_with_random_target(agent1_interface, random_target_agent1)
        communicate_with_random_target(agent2_interface, random_target_agent2)
        communicate_with_random_target(agent3_interface, random_target_agent3)

        # Deactivate the sniffer after communication
        sniff_active_agent1.clear()
        sniff_active_agent2.clear()
        sniff_active_agent3.clear()

    agent_listener_thread1.join()
    agent_listener_thread2.join()
    agent_listener_thread3.join()
