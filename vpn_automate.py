# import pandas as pd
# import subprocess
# import time

# # df = pd.read_csv('state.csv')

# # with open('login.txt', 'r') as f:
# #     lines = f.readlines()
# #     username = lines[0].strip()
# #     password = lines[1].strip()

# def login_vpn(username, password):
#     # Full path to piactl.exe
#     piactl_path = r"C:\Program Files\Private Internet Access"
    
#     # Example command to login
#     login_command = [".\\piactl", "login", "--username", username, "--password", password]
    
#     # Run the command
#     result = subprocess.run(login_command, capture_output=True, text=True)
    
#     if result.returncode == 0:
#         print("VPN login successful")
#     else:
#         print(f"Error: {result.stderr}")

def get_vpn_ip():
    result = subprocess.run(['curl', 'https://ipinfo.io/ip'], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return "Unable to retrieve IP address"

# def check_vpn_status():
#     result = subprocess.run(['piactl', 'get', 'connectionstate'], capture_output=True, text=True)
#     return result.stdout.strip()

# # def connect_vpn(state):

# #     state_to_server = {
# #         'California': 'us-west',
# #         'New York': 'us-east',
# #         # TODO: Add more states
# #     }
    
# #     server = state_to_server.get(state, None)
# #     if server:
# #         disconnect_command = ['piactl', 'disconnect']
# #         subprocess.run(disconnect_command)
# #         print(f"Disconnected from any active VPN session.")
        
# #         while check_vpn_status() != 'Disconnected':
# #             print("Waiting for VPN to disconnect...")
# #             time.sleep(2)
        
# #         # Set the new server region
# #         set_server_command = ['piactl', 'set', 'region', server]
# #         subprocess.run(set_server_command)
# #         print(f"Set the region to {server} for {state}.")
        
# #         # Initiate the connection
# #         connect_command = ['piactl', 'connect']
# #         subprocess.run(connect_command)
# #         print(f"Attempting to connect to the VPN server in {state} ({server})...")
        
# #         # Wait until the VPN is fully connected
# #         connection_attempts = 0
# #         max_attempts = 10
# #         while check_vpn_status() != 'Connected' and connection_attempts < max_attempts:
# #             print("Waiting for VPN to connect...")
# #             time.sleep(2) 
# #             connection_attempts += 1
        
# #         if check_vpn_status() == 'Connected':
# #             vpn_ip = get_vpn_ip()
# #             print(f"Connected successfully. VPN IP Address: {vpn_ip}")
# #         else:
# #             print(f"Failed to connect to {server} after {max_attempts} attempts.")
# #     else:
# #         print(f"No server found for state: {state}")

# def change_vpn(state, server):
#     if check_vpn_status() != 'Connected' or get_vpn_ip() != server:
#         connect_command = ['piactl', 'connect', server]
#         subprocess.run(connect_command)
#         print(f"Connecting to VPN for {state} ({server})...")

#         # Wait until VPN is connected
#         attempts = 0
#         max_attempts = 5
#         while check_vpn_status() != 'Connected' and attempts < max_attempts:
#             print("Waiting for VPN to connect...")
#             time.sleep(2)
#             attempts += 1

#         if check_vpn_status() == 'Connected':
#             vpn_ip = get_vpn_ip()
#             print(f"Connected successfully. VPN IP: {vpn_ip}")
#             return vpn_ip
#         else:
#             print(f"Failed to connect to {server} after {max_attempts} attempts.")
#             return None
#     else:
#         return get_vpn_ip()

import subprocess
import time

# Provide the full path to piactl
PIA_PATH = r'C:\Program Files\Private Internet Access\piactl.exe'

# Function to log in to the VPN using username and password
def login_vpn(username, password):
    login_command = [PIA_PATH, 'login', '--username', username, '--password', password]
    result = subprocess.run(login_command, capture_output=True, text=True)
    if result.returncode == 0:
        print("Login successful.")
    else:
        print(f"Failed to log in: {result.stderr}")

# Function to check VPN connection status
def check_vpn_status():
    result = subprocess.run([PIA_PATH, "get", "connectionstate"], capture_output=True, text=True)
    return result.stdout.strip()

# Function to get the current VPN IP
# def get_vpn_ip():
#     result = subprocess.run([PIA_PATH, "get", "ip"], capture_output=True, text=True)
#     return result.stdout.strip()

# Function to change VPN based on the pia_vpn value from CSV
def change_vpn(pia_vpn):
    if check_vpn_status() != 'Connected' or get_vpn_ip() != pia_vpn:
        # Step 1: Set the region
        set_region_command = [PIA_PATH, 'set', 'region', pia_vpn]
        subprocess.run(set_region_command)
        print(f"Region set to {pia_vpn}.")
        time.sleep(5)

        # Step 2: Connect to the VPN
        connect_command = [PIA_PATH, 'connect']
        subprocess.run(connect_command)
        print(f"Connecting to VPN...")
        time.sleep(5)

        # Wait for VPN to connect
        attempts = 0
        max_attempts = 20  # Increased the max attempts
        while check_vpn_status() != 'Connected' and attempts < max_attempts:
            print("Waiting for VPN to connect...")
            time.sleep(5)  # Increased the wait time to 5 seconds
            attempts += 1

        if check_vpn_status() == 'Connected':
            vpn_ip = get_vpn_ip()
            print(f"Connected successfully. VPN IP: {vpn_ip}")
            return vpn_ip
        else:
            print(f"Failed to connect to {pia_vpn} after {max_attempts} attempts.")
            return None
    else:
        return get_vpn_ip()
