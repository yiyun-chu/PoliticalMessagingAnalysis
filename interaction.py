import base64
import os.path
import random
import re
import csv
import math
import time
from dateutil import parser
# import schedule
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from selenium import webdriver
from datetime import datetime, timedelta
import pytz

eastern = pytz.timezone('US/Eastern')
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

USER_TOKENS = 'token.json'
CREDENTIALS = 'credentials.json'
url_pattern = r'(https?://[^\s]+)'

LAST_OPENED_EMAIL_TIME_FILE = 'last_opened_email_time.txt'
CSV_FILE = 'processed_emails.csv'

def get_last_opened_email_time():
    if os.path.exists('last_opened_email_time.txt'):
        with open('last_opened_email_time.txt', 'r') as f:
            last_time_str = f.read().strip()
            last_opened_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")
            last_opened_time = eastern.localize(last_opened_time)
            return last_opened_time
    else:
        print("No previous email open time found. Processing all emails.")
        return eastern.localize(datetime(1970, 1, 1))  

def save_last_opened_email_time(last_opened_time):
    last_opened_time = last_opened_time.astimezone(eastern)
    with open('last_opened_email_time.txt', 'w') as f:
        f.write(last_opened_time.strftime("%Y-%m-%d %H:%M:%S"))

def extract_links(email_body):
    links = re.findall(url_pattern, email_body)
    return [link for link in links if not link.endswith('.gif')]

def open_link_in_browser(link):
    driver = webdriver.Chrome() 
    driver.get(link)
    print(f"Opening link in browser: {link}")
    time.sleep(5)
    driver.quit()

def heaviside(x):
    return 1 if x > 0 else 0

def should_click_link(k):
    x = random.random()
    heaviside_input = math.sin(2 * math.pi * x) - math.cos(math.pi * x / k)
    heaviside_output = heaviside(heaviside_input)
    return heaviside_output, k, heaviside_input

def get_credentials():
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

def fetch_emails(service, last_opened_time):
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
            date_received_str = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Date'), None)

            if date_received_str:
                try:
                    # Parse the date_received as an offset-aware datetime
                    date_received = parser.parse(date_received_str)
                    date_received = date_received.astimezone(eastern)
                    
                    if date_received > last_opened_time:
                        email_bodies.append({
                            'id': message['id'],
                            'text': email_data,
                            'subject': subject,
                            'from': from_email,
                            'date_received': date_received
                        })
                except ValueError as e:
                    print(f"Date parsing error: {e}")
        return email_bodies
    except Exception as error:
        print(f'An error occurred while fetching emails: {error}')
        return []
    
def parse_msg(msg):
    payload = msg['payload']
    if 'body' in payload and payload['body'].get('data'):
        return base64.urlsafe_b64decode(payload['body']['data'].encode('ASCII')).decode('utf-8')
    elif 'parts' in payload:
        parts = payload['parts']
        data = next((part['body']['data'] for part in parts if part['mimeType'] == 'text/plain'), None)
        if data:
            return base64.urlsafe_b64decode(data.encode('ASCII')).decode('utf-8')
    return ""

def process_emails(service):
    last_opened_time = get_last_opened_email_time()
    email_bodies = fetch_emails(service, last_opened_time)

    if not email_bodies:
        print("No new emails to process.")
        return

    first_opened_email_time = None

    for email in email_bodies:
        print(f"Processing email ID: {email['id']}")
        print(f"Subject: {email['subject']}")
        print(f"From: {email['from']}")
        print(f"Received at: {email['date_received']}")

        try:
            service.users().messages().modify(userId='me', id=email['id'], body={'removeLabelIds': ['UNREAD']}).execute()

            links = extract_links(email['text'])
            priority_links = [link for link in links if any(keyword in link.lower() for keyword in ['ngpvan', 'actblue', 'winred']) or re.search(r'(\$|donate)', link, re.IGNORECASE)]
            other_links = [link for link in links if 'unsubscribe' not in link.lower() and link not in priority_links]

            link_clicked = False
            clicked_link = None  # To store the actual clicked link
            k = random.uniform(0.5, 2.0)  # Randomly choose 'motivation' factor
            heaviside_output, k_value, heaviside_input = should_click_link(k)
            if heaviside_output:
                if priority_links:
                    clicked_link = priority_links[0]
                    open_link_in_browser(clicked_link)
                    link_clicked = True
                elif other_links:
                    clicked_link = other_links[0]
                    open_link_in_browser(clicked_link)
                    link_clicked = True
                else:
                    print("No suitable links found in this email.")
            else:
                print("Decided not to click any links in this email.")

            append_to_csv(email, True, link_clicked, k_value, heaviside_input, heaviside_output, clicked_link)

            if first_opened_email_time is None:
                first_opened_email_time = email['date_received']

        except Exception as e:
            print(f"Error processing email ID: {email['id']}: {e}")

    if first_opened_email_time:
        save_last_opened_email_time(first_opened_email_time)

def append_to_csv(email, opened, link_clicked, k_value, heaviside_input, heaviside_output, clicked_link):
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'subject', 'from', 'date_received', 'text', 'link', 'clicked_link', 'opened', 'link_clicked', 'k_value', 'heaviside_input', 'heaviside_output', 'timestamp'])
        if not file_exists:
            writer.writeheader()

        links = extract_links(email['text'])
        first_link = links[0] if links else None

        writer.writerow({
            'id': email['id'],
            'subject': email['subject'],
            'from': email['from'],
            'date_received': email['date_received'].isoformat(),
            'text': email['text'],
            'link': first_link,
            'clicked_link': clicked_link,  # Ensure this field is included
            'opened': int(opened),
            'link_clicked': int(link_clicked),
            'k_value': k_value,
            'heaviside_input': heaviside_input,
            'heaviside_output': heaviside_output,
            'timestamp': datetime.now(pytz.UTC).astimezone(eastern).isoformat()
        })

def run_email_processing():
    print(f"Starting email processing at {datetime.now(pytz.UTC).astimezone(eastern).isoformat()}")
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)
    try:
        process_emails(service)
    except Exception as e:
        print(f"An error occurred during email processing: {e}")
    finally:
        print(f"Finished email processing at {datetime.now(pytz.UTC).astimezone(eastern).isoformat()}")

def main():
    # Schedule the job to run every 2 hours
    # schedule.every(2).hours.do(run_email_processing)

    # Run the job immediately once
    run_email_processing()

    # Keep the script running and check for scheduled jobs
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)  # Wait for one minute before checking again

if __name__ == '__main__':
    main()