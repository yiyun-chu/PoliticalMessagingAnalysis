import os
import random
import re
import csv
import base64
from datetime import datetime
import pandas as pd
from dateutil import parser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pytz
import time
import platform
import subprocess
import json
from scipy.stats import beta

eastern = pytz.timezone('US/Eastern')

# Gmail API
SCOPES = ['YOUR_GMAIL_API_SCOPE']

# File paths
USER_TOKENS = 'YOUR_GMAIL_TOKEN.json'
CREDENTIALS = 'YOUR_GMAIL_CREDENTIALS.json'
LAST_OPENED_EMAIL_TIME_FILE = 'TRACK_LAST_INTERACTION_TIME.txt'
CSV_FILE = 'TRACK_INTERACTION.csv'
FULL_DATAFRAME_FILE = 'YOUR_DATA_INPUT.csv'
PROCESSING_LOG_FILE = 'LOG_FILE.csv'
EMAIL_RECIPIENT_PATTERN = r'\+([a-zA-Z0-9]+)@'

def load_full_dataframe():
    """Load the input dataframe mapping UUIDs to base_vpn, alpha, beta, and check_email_freq."""
    if not os.path.exists(FULL_DATAFRAME_FILE):
        print(f"Input Data '{FULL_DATAFRAME_FILE}' not found.")
        return pd.DataFrame()
    try:
        df = pd.read_csv(FULL_DATAFRAME_FILE)
        return df
    except Exception as e:
        print(f"Error loading dataframe: {e}")
        return pd.DataFrame()
    
def get_last_processed_time(uuid):
    """Retrieve the last opened email time for a specific UUID."""
    if os.path.exists(LAST_OPENED_EMAIL_TIME_FILE):
        with open(LAST_OPENED_EMAIL_TIME_FILE, 'r') as f:
            last_times = json.load(f)
            if uuid in last_times:
                last_time_str = last_times[uuid]
                try:
                    last_opened_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")
                    last_opened_time = eastern.localize(last_opened_time)
                    return last_opened_time
                except ValueError:
                    print(f"Error parsing the last opened email time for UUID {uuid}. Resetting to epoch.")
    else:
        print("No previous email open times found. Processing all emails.")
    return eastern.localize(datetime(1970, 1, 1))  # Default to epoch time

def save_last_processed_time(uuid, last_opened_time):
    """Save the last opened email time for a specific UUID."""
    last_opened_time = last_opened_time.astimezone(eastern)
    if os.path.exists(LAST_OPENED_EMAIL_TIME_FILE):
        with open(LAST_OPENED_EMAIL_TIME_FILE, 'r') as f:
            last_times = json.load(f)
    else:
        last_times = {}

    last_times[uuid] = last_opened_time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LAST_OPENED_EMAIL_TIME_FILE, 'w') as f:
        json.dump(last_times, f, indent=4)

def get_credentials():
    """Authenticate and return Gmail API credentials."""
    creds = None
    if os.path.exists(USER_TOKENS):
        creds = Credentials.from_authorized_user_file(USER_TOKENS, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(USER_TOKENS, 'w') as token:
            token.write(creds.to_json())
    return creds

def move_all_emails_to_inbox(service):
    """Move all emails from Spam, Promotions, Social, etc., into the Inbox."""
    labels_to_move = ['SPAM', 'CATEGORY_PROMOTIONS', 'CATEGORY_SOCIAL', 'CATEGORY_UPDATES', 'CATEGORY_FORUMS']

    for label in labels_to_move:
        try:
            results = service.users().messages().list(userId='me', labelIds=[label]).execute()
            messages = results.get('messages', [])

            if not messages:
                print(f"No messages found in {label}.")
                continue

            for message in messages:
                print(f"Moving message ID: {message['id']} from {label} to INBOX")
                service.users().messages().modify(userId='me', id=message['id'],
                                                    body={'addLabelIds': ['INBOX'], 'removeLabelIds': [label]}).execute()

            print(f"All emails from {label} have been moved to the INBOX.")
        
        except Exception as error:
            print(f"An error occurred while moving emails from {label}: {error}")
    print("Finished moving all relevant emails to INBOX.")

def fetch_emails(service, last_opened_time):
    """Fetch emails received after the last opened time."""
    try:
        query = f'after:{int(last_opened_time.timestamp())}'
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q=query).execute()
        messages = results.get('messages', [])
        if not messages:
            print('No new messages.')
            return []

        email_bodies = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email_data = parse_msg(msg)
            subject = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'), 'No Subject')
            from_email = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'From'), 'Unknown Sender')
            to_email = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'To'), 'Unknown Recipient')
            date_received_str = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Date'), None)

            if date_received_str:
                try:
                    date_received = parser.parse(date_received_str)
                    date_received = date_received.astimezone(eastern)
                    
                    if date_received > last_opened_time:
                        email_bodies.append({
                            'id': message['id'],
                            'text': email_data,
                            'subject': subject,
                            'from': from_email,
                            'to': to_email,
                            'date_received': date_received
                        })
                except ValueError as e:
                    print(f"Date parsing error: {e}")
        return email_bodies
    except Exception as error:
        print(f'An error occurred while fetching emails: {error}')
        return []
    
def parse_msg(msg):
    """Parse the email message to extract the body text."""
    payload = msg['payload']
    if 'body' in payload and payload['body'].get('data'):
        return base64.urlsafe_b64decode(payload['body']['data'].encode('ASCII')).decode('utf-8')
    elif 'parts' in payload:
        parts = payload['parts']
        data = next((part['body']['data'] for part in parts if part['mimeType'] == 'text/plain'), None)
        if data:
            return base64.urlsafe_b64decode(data.encode('ASCII')).decode('utf-8')
    return ""

def extract_uuid(to_email):
    """Extract UUID from the recipient's email address."""
    match = re.search(EMAIL_RECIPIENT_PATTERN, to_email)
    if match:
        return match.group(1)
    else:
        print(f"UUID not found in recipient email: {to_email}")
        return None

def extract_uuids_from_emails(email_bodies):
    """Extract UUIDs from the list of emails."""
    uuids = []
    for email in email_bodies:
        uuid = extract_uuid(email['to'])
        if uuid:
            uuids.append(uuid)
    return uuids

def filter_emails_after_last_processed(email_bodies, last_processed_time):
    """Filter emails that are received after the last processed time."""
    new_emails = []
    for email in email_bodies:
        if email['date_received'] > last_processed_time:
            new_emails.append(email)
    return new_emails

def log_processing_event(start_time, end_time, status_message, sleep_minutes):
    """Append a new row to the processing_log.csv with event details."""
    file_exists = os.path.exists(PROCESSING_LOG_FILE)
    with open(PROCESSING_LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['start_time', 'end_time', 'status_message', 'sleep_minutes']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'status_message': status_message,
            'sleep_minutes': round(sleep_minutes, 2)
        })

def random_check_personas(full_df, uuid, random_threshold):
    """Randomly decide whether to check emails based on check_email_freq."""
    persona_data = full_df[full_df['uuid'] == uuid]
    if not persona_data.empty:
        check_email_freq = persona_data.iloc[0]['check_email_freq']

        if check_email_freq > random_threshold:
            return True, check_email_freq
        else:
            return False, check_email_freq
    return False, 0

def process_email_rules(email, full_df, uuid):
    """Process email open and click based on alpha-beta distribution."""
    persona_data = full_df[full_df['uuid'] == uuid]
    if not persona_data.empty:
        alpha = persona_data.iloc[0]['alpha']
        beta_val = persona_data.iloc[0]['beta']
        
        beta_flip = beta.rvs(alpha, beta_val)        
        random_draw = random.random()
        action = random_draw < beta_flip

        return action, beta_flip, random_draw
    return False, 0, 0
            
def process_emails_in_batches(service, full_df):
    """Process emails in batches based on the uuid and VPN region."""
    move_all_emails_to_inbox(service)
    
    email_bodies = fetch_emails(service, get_last_processed_time('1970-01-01'))
    uuids = extract_uuids_from_emails(email_bodies)
    
    if not uuids:
        print("No UUIDs found in the emails.")
        return "No UUIDs found in the emails."

    random_threshold = random.random()
    
    # Apply the random_check_personas rule to decide which personas to process
    uuids_to_process = []
    for uuid in uuids:
        should_process, check_email_freq = random_check_personas(full_df, uuid, random_threshold)
        if should_process:
            uuids_to_process.append((uuid, random_threshold, check_email_freq))
    
    log_str = ', '.join([f"{uuid} (random_threshold={threshold:.4f}, check_email_freq={freq:.4f})" 
                        for uuid, threshold, freq in set(uuids_to_process)])
    if log_str:
        print(f"UUIDs to process: {log_str}")
    else:
        print("No UUIDs passed the random check threshold.")
        return "No UUIDs to process."

    if not uuids_to_process:
        print("No UUIDs passed the random check threshold.")
        return "No UUIDs to process."

    # Filter emails for personas that passed the random check
    email_bodies_by_uuid = {}
    for uuid, random_threshold, check_email_freq in uuids_to_process:
        last_processed_time = get_last_processed_time(uuid)
        new_emails = filter_emails_after_last_processed(email_bodies, last_processed_time)

        if new_emails:
            email_bodies_by_uuid[uuid] = {
                'emails': new_emails,
                'random_threshold': random_threshold,
                'check_email_freq': check_email_freq
            }
    if not email_bodies_by_uuid:
        print("No new emails to process after filtering.")
        return "No new emails to process."

    # Group emails by pia_vpn
    emails_by_vpn = {}
    for uuid, data in email_bodies_by_uuid.items():
        for email in data['emails']:
            user_data = full_df[full_df['uuid'] == uuid]
            if not user_data.empty:
                pia_vpn = user_data.iloc[0]['pia_vpn']
                base_vpn = user_data.iloc[0]['base_vpn']
                if pia_vpn not in emails_by_vpn:
                    emails_by_vpn[pia_vpn] = []
                emails_by_vpn[pia_vpn].append((email, uuid, data['random_threshold'], data['check_email_freq']))

    processed_count = 0
    most_recent_email_time = None

    for pia_vpn, emails_uuid_data in emails_by_vpn.items():
        print(f"Setting VPN region to: {pia_vpn}")
        change_vpn(pia_vpn)
        time.sleep(3)

        for email, uuid, random_threshold, check_email_freq in emails_uuid_data:
            try:
                user_data = full_df[full_df['uuid'] == uuid]

                if user_data.empty:
                    continue

                # Beta Distribution for email open and click
                opened, open_bias_flip, open_random_draw = process_email_rules(email, full_df, uuid)
                time_opened = None

                if opened:
                    service.users().messages().modify(userId='me', id=email['id'], body={'removeLabelIds': ['UNREAD']}).execute()
                    print(f"Email ID: {email['id']} marked as read (opened).")
                    processed_count += 1
                    time_opened = datetime.now(pytz.UTC).astimezone(eastern)

                append_to_csv(email, uuid, check_email_freq, random_threshold, pia_vpn, open_bias_flip, open_random_draw, opened, time_opened)

                if most_recent_email_time is None or most_recent_email_time < email['date_received']:
                    most_recent_email_time = email['date_received']

            except Exception as e:
                print(f"Error processing email ID: {email['id']}: {e}")

    if most_recent_email_time:
        for uuid in email_bodies_by_uuid.keys():
            save_last_processed_time(uuid, most_recent_email_time)
            
    status_message = f"Processed {processed_count} new emails across all UUIDs."
    if log_str:
        status_message += f"\nUUIDs processed: {log_str}"
    return status_message

def append_to_csv(email, uuid, check_email_freq, random_threshold, pia_vpn, open_bias_flip, open_random_draw, opened, time_opened):
    """Append the processing result to the processed_emails.csv file."""
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = [
            'id', 'subject', 'from', 'to', 'uuid', 'date_received', 'check_email_freq', 'check_email_threshold', 
            'pia_vpn', 'open_beta_flip', 'open_random_draw', 'is_opened', 'open_time', 'timestamp', 'body_text'
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'id': email['id'],
            'subject': email['subject'],
            'from': email['from'],
            'to': email['to'],
            'uuid': uuid,
            'date_received': email['date_received'].isoformat(),
            'check_email_freq': check_email_freq,
            'check_email_threshold': random_threshold,
            'pia_vpn': pia_vpn,
            'open_beta_flip': open_bias_flip,
            'open_random_draw': open_random_draw,
            'is_opened': int(opened),
            'open_time': time_opened,
            'timestamp': datetime.now(pytz.UTC).astimezone(eastern).isoformat(),
            'body_text': email['text']
        })

def run_email_processing():
    """Run the entire email processing workflow."""
    print(f"\nStarting email processing at {datetime.now(pytz.UTC).astimezone(eastern).isoformat()}")
    start_time = datetime.now(pytz.UTC).astimezone(eastern)

    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)
    full_df = load_full_dataframe()
    if full_df.empty:
        print("Full dataframe is empty or could not be loaded. Exiting processing.")
        end_time = datetime.now(pytz.UTC).astimezone(eastern)
        status_message = "Full dataframe is empty or could not be loaded."
        sleep_minutes = 0
        log_processing_event(start_time, end_time, status_message, sleep_minutes)
        return

    try:
        status_message = process_emails_in_batches(service, full_df)
    except Exception as e:
        print(f"An error occurred during email processing: {e}")
        status_message = f"An error occurred: {e}"
    finally:
        end_time = datetime.now(pytz.UTC).astimezone(eastern)
        print(f"Finished email processing at {end_time.isoformat()}")

    sleep_seconds = random.randint(60, 1800)
    sleep_minutes = sleep_seconds / 60
    
    print(f"Sleeping for {sleep_minutes:.2f} minutes before next run.")

    log_processing_event(start_time, end_time, status_message, sleep_minutes)

    return sleep_minutes

def log_processing_event(start_time, end_time, status_message, sleep_minutes):
    """Append a new row to the processing_log.csv with event details."""
    file_exists = os.path.exists(PROCESSING_LOG_FILE)
    with open(PROCESSING_LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['start_time', 'end_time', 'status_message', 'sleep_minutes']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'status_message': status_message,
            'sleep_minutes': round(sleep_minutes, 2)
        })

#### VPN Automation ####
if platform.system() == "Windows":
    PIA_PATH = 'YOUR_PIA_PATH'
else:
    PIA_PATH = 'YOUR_PIA_PATH_FOR_MAC'
    
def login_vpn(username, password):
    login_command = [PIA_PATH, 'login', '--username', username, '--password', password]
    result = subprocess.run(login_command, capture_output=True, text=True)
    if result.returncode == 0:
        print("Login successful.")
    else:
        print(f"Already logged in: {result.stderr}")
    
def check_vpn_status():
    result = subprocess.run([PIA_PATH, "get", "connectionstate"], capture_output=True, text=True)
    return result.stdout.strip()

def get_vpn_ip():
    result = subprocess.run(['curl', 'https://ipinfo.io/ip'], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return "Unable to retrieve IP address"

def change_vpn(pia_vpn):
    if check_vpn_status() != 'Connected' or get_vpn_ip() != pia_vpn:
        # Set the region
        set_region_command = [PIA_PATH, 'set', 'region', pia_vpn]
        subprocess.run(set_region_command)
        print(f"Region set to {pia_vpn}.")
        time.sleep(5)

        #  Connect to the VPN
        connect_command = [PIA_PATH, 'connect']
        subprocess.run(connect_command)
        print(f"Connecting to VPN...")
        time.sleep(5) 
        
        attempts = 0
        max_attempts = 10
        while check_vpn_status() != 'Connected' and attempts < max_attempts:
            print("Waiting for VPN to connect...")
            time.sleep(5)
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
        
def main():
    """Run the email processing workflow once."""
    print("Email processing script started.")
    try:
        creds = get_credentials()
        service = build('gmail', 'v1', credentials=creds)
        full_df = load_full_dataframe()

        if full_df.empty:
            print("Full dataframe is empty or could not be loaded. Exiting processing.")
            return

        start_time = datetime.now(pytz.UTC).astimezone(eastern)
        try:
            status_message = process_emails_in_batches(service, full_df)
        except Exception as e:
            print(f"An error occurred during email processing: {e}")
            status_message = f"An error occurred: {e}"
        finally:
            end_time = datetime.now(pytz.UTC).astimezone(eastern)
            print(f"Finished email processing at {end_time.isoformat()}")

        log_processing_event(start_time, end_time, status_message, 0)

    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting gracefully.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Email processing script terminated.")

if __name__ == '__main__':
    main()           
