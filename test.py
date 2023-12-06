import subprocess
import time
import os
import signal 
# import datetime


# 1. Create a subprocess that runs arpspoof.py
def test():
    # print(datetime.now())
    process = subprocess.Popen([f'python3 arpspoof.py --targetip 10.21.0.12 -i Melchior --attackermac F6:91:7F:74:12:F6 --targetmac 12:45:6C:CD:58:D6 --gatewaymac DE:BC:50:A7:AD:9E -f'], shell=True, preexec_fn=os.setsid)  
    time.sleep(60)

    os.killpg(os.getpgid(process.pid),signal.SIGTERM)
    #process.kill()

test()
# 2. Wait x amount of time (2 minutes)

# 3. Kill the subprocess

# This tests 1. Can we kill subprocesses, 2. Are you waiting properly (I don't think sleeps do)
# 3. Gives you only ONE spot to modify (working in a known good environment instead of the arp-poisoner.py)



