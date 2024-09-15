from __future__ import print_function
import base64
import os.path
import random
import re
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from selenium import webdriver
import time
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

USER_TOKENS = 'token.json'
CREDENTIALS = 'credentials.json'
url_pattern = r'(https?://[^\s]+)'

LAST_RUN_FILE = 'last_run_time.txt'

# Record the timestamp of the last email run
def get_last_run_time():
    if os.path.exists(LAST_RUN_FILE):
        with open(LAST_RUN_FILE, 'r') as f:
            return datetime.fromisoformat(f.read().strip())
    return None

def save_last_run_time(last_run_time):
    with open(LAST_RUN_FILE, 'w') as f:
        f.write(last_run_time.isoformat())

def get_credentials():
    creds = None
    if os.path.exists(USER_TOKENS):
        creds = Credentials.from_authorized_user_file(USER_TOKENS, SCOPES)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(USER_TOKENS, 'w') as token:
            token.write(creds.to_json())
    return creds

def fetch_emails(service, last_run_time):
    try:
        query = f"after:{int(last_run_time.timestamp())}" if last_run_time else None
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q=query).execute()
        messages = results.get('messages', [])
        if not messages:
            print('No new messages.')
            return []
        email_bodies = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email_data = parse_msg(msg)
            subject = next(header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject')
            from_email = next(header['value'] for header in msg['payload']['headers'] if header['name'] == 'From')
            date_received = next(header['value'] for header in msg['payload']['headers'] if header['name'] == 'Date')
            email_bodies.append({
                'id': message['id'],
                'text': email_data,
                'subject': subject,
                'from': from_email,
                'date_received': date_received
            })
        return email_bodies
    except Exception as error:
        print(f'An error occurred while fetching emails: {error}')
        return []

def parse_msg(msg):
    payload = msg['payload']
    if data := payload['body'].get('data'):
        return parse_data(data)

    return ''.join(parse_data(part['body']['data']) for part in payload['parts'] if part['mimeType'] != 'image/gif')

def parse_data(data):
    return base64.urlsafe_b64decode(data.encode('ASCII')).decode('utf-8')

def extract_links(email_body):
    """Extracts all URLs from the email body, excluding .gif links."""
    links = re.findall(url_pattern, email_body)
    return [link for link in links if not link.endswith('.gif')]

def open_link_in_browser(link):
    """Opens a URL in the browser using Selenium."""
    driver = webdriver.Chrome() 
    driver.get(link)
    print(f"Opening link in browser: {link}")
    time.sleep(5)
    driver.quit()

def random_action_on_emails(email_bodies, service):
    for email in email_bodies:
        if random.choice([True, False]):
            print(f"Randomly decided to process email ID: {email['id']}")
            print(f"Subject: {email['subject']}")
            print(f"From: {email['from']}")
            print(f"Received at: {email['date_received']}")
            print(f"Body: {email['text']}")
            
            service.users().messages().modify(userId='me', id=email['id'], body={'removeLabelIds': ['UNREAD']}).execute()
            
            links = extract_links(email['text'])
            if links:
                first_link = links[0]  # Click the first link found
                open_link_in_browser(first_link)
            else:
                print("No links found in this email.")
        else:
            print(f"Randomly decided to skip email ID: {email['id']}")

def main():
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    last_run_time = get_last_run_time()
    email_bodies = fetch_emails(service, last_run_time)

    if email_bodies:
        random_action_on_emails(email_bodies, service)

    # Save the current time for future runs
    save_last_run_time(datetime.now())

if __name__ == '__main__':
    main()
