import pandas as pd
import subprocess
import time

# df = pd.read_csv('state.csv')

with open('login.txt', 'r') as f:
    lines = f.readlines()
    username = lines[0].strip()
    password = lines[1].strip()

def get_vpn_ip():
    result = subprocess.run(['curl', 'https://ipinfo.io/ip'], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return "Unable to retrieve IP address"

def check_vpn_status():
    result = subprocess.run(['piactl', 'get', 'connectionstate'], capture_output=True, text=True)
    return result.stdout.strip()

def connect_vpn(state):

    state_to_server = {
        'California': 'us-west',
        'New York': 'us-east',
        # TODO: Add more states
    }
    
    server = state_to_server.get(state, None)
    if server:
        disconnect_command = ['piactl', 'disconnect']
        subprocess.run(disconnect_command)
        print(f"Disconnected from any active VPN session.")
        
        while check_vpn_status() != 'Disconnected':
            print("Waiting for VPN to disconnect...")
            time.sleep(2)
        
        # Set the new server region
        set_server_command = ['piactl', 'set', 'region', server]
        subprocess.run(set_server_command)
        print(f"Set the region to {server} for {state}.")
        
        # Initiate the connection
        connect_command = ['piactl', 'connect']
        subprocess.run(connect_command)
        print(f"Attempting to connect to the VPN server in {state} ({server})...")
        
        # Wait until the VPN is fully connected
        connection_attempts = 0
        max_attempts = 10
        while check_vpn_status() != 'Connected' and connection_attempts < max_attempts:
            print("Waiting for VPN to connect...")
            time.sleep(2) 
            connection_attempts += 1
        
        if check_vpn_status() == 'Connected':
            vpn_ip = get_vpn_ip()
            print(f"Connected successfully. VPN IP Address: {vpn_ip}")
        else:
            print(f"Failed to connect to {server} after {max_attempts} attempts.")
    else:
        print(f"No server found for state: {state}")