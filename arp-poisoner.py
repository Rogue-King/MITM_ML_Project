import subprocess
import threading
import random
import time
import sys
from datetime import datetime, timedelta

INTERFACES = ['Melchior', 'Balthasar', 'Casper']
TARGET_INTERFACES = ['Maria', 'Rose', 'Sina']

# Data structure for agents
agents_info = {
    'Melchior': {'interface_mac': 'F6:91:7F:74:12:F6'},
    'Balthasar': {'interface_mac': 'F2:C7:F1:B6:80:98'},
    'Casper': {'interface_mac': 'B2:DE:93:F3:CD:F8'}
}

# Data structure for targets
targets_info = {
    'Maria': {'target_mac': 'CE:32:51:9F:81:02'},
    'Rose': {'target_mac': '12:45:6C:CD:58:D6'},
    'Sina': {'target_mac': 'B2:DA:BF:0C:ED:AB'}
}

# Number of agents
num_agents = len(INTERFACES)

# Lock for the availability of interfaces
interface_lock = [threading.Lock() for _ in range(num_agents)]

# Function to simulate code execution on an interface
def execute_code(agent_id, target_interface): # ARP-poison script: https://github.com/EONRaider/Arp-Spoofer
    agent_name = INTERFACES[agent_id]
    agent_interface_mac = agents_info[agent_name]['interface_mac']

    with interface_lock[agent_id]:
        print(f"Agent {agent_name} ({agent_id}) is executing code on {target_interface}.")
        print(f"Agent {agent_name}'s Interface MAC: {agent_interface_mac}")

        # Generate a random duration between 2 to 4 minutes
        duration = random.uniform(2, 4)
        end_time = datetime.now() + timedelta(minutes=duration)

        # Run the loop until the specified end time
        while datetime.now() < end_time:
            # Simulate code execution by doing some work
            # (Replace this with the actual code execution logic)
            time.sleep(1)  # Simulating work for 1 second

    print(f"Agent {agent_name} finished executing code on {target_interface}.")


# Function to run an agent
def run_agent(agent_id):
    while True:
        # Choose a random target interface
        target_interface = random.choice(TARGET_INTERFACES)

        # Remove the used target interface
        TARGET_INTERFACES.remove(target_interface)

        # Execute code on the chosen interface
        execute_code(agent_id, target_interface)

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
        time.sleep(60 * 60)
    except KeyboardInterrupt:
        print("\nReceived KeyboardInterrupt. Stopping agents...")
        sys.exit()

    # Stop the agents by joining the threads
    for thread in threads:
        thread.join()

# Entry point
if __name__ == "__main__":
    main()
