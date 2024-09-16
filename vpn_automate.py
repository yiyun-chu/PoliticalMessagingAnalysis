import subprocess
import time

PIA_PATH = r'C:\Program Files\Private Internet Access\piactl.exe'

# Log in to the VPN using username and password
def login_vpn(username, password):
    login_command = [PIA_PATH, 'login', '--username', username, '--password', password]
    result = subprocess.run(login_command, capture_output=True, text=True)
    if result.returncode == 0:
        print("Login successful.")
    else:
        print(f"Failed to log in: {result.stderr}")

# Check VPN connection status
def check_vpn_status():
    result = subprocess.run([PIA_PATH, "get", "connectionstate"], capture_output=True, text=True)
    return result.stdout.strip()

# Get the VPN IP
def get_vpn_ip():
    result = subprocess.run(['curl', 'https://ipinfo.io/ip'], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return "Unable to retrieve IP address"
    
# Change VPN based on the pia_vpn value from CSV
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
