import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def create_driver(profile_path):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-data-dir={profile_path}")
    # driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)
    chrome_service = Service(executable_path = '/Users/athena/Desktop/Research/election/chromedriver-mac-arm64/chromedriver')
    return webdriver.Chrome(service=chrome_service, options=chrome_options) #webdriver.Chrome(options=chrome_service)

# Define profiles and URLs
# profiles = [
#     "/Users/athena/Library/Application Support/Google/Chrome/Profile 12",
#     "/Users/athena/Library/Application Support/Google/Chrome/profile100",
# ]

profiles = [
    "/Users/athena/Library/Application Support/Google/Chrome/dup01",
    "/Users/athena/Library/Application Support/Google/Chrome/dup02",
    "/Users/athena/Library/Application Support/Google/Chrome/dup03",
    "/Users/athena/Library/Application Support/Google/Chrome/dup04",
    "/Users/athena/Library/Application Support/Google/Chrome/dup05",
    "/Users/athena/Library/Application Support/Google/Chrome/dup06",
    "/Users/athena/Library/Application Support/Google/Chrome/dup07",
    "/Users/athena/Library/Application Support/Google/Chrome/dup08",
    "/Users/athena/Library/Application Support/Google/Chrome/dup09",
    "/Users/athena/Library/Application Support/Google/Chrome/dup10",
    "/Users/athena/Library/Application Support/Google/Chrome/dup11",
    "/Users/athena/Library/Application Support/Google/Chrome/dup12",
    "/Users/athena/Library/Application Support/Google/Chrome/dup13",
    "/Users/athena/Library/Application Support/Google/Chrome/dup14",
    "/Users/athena/Library/Application Support/Google/Chrome/dup15"
    ]

urls = [
    "https://erichovde.com",
    "https://kamalaharris.com",
    "https://berniemoreno.com",
    "https://erichovde.com",
    "https://kamalaharris.com",
    "https://berniemoreno.com",
    "https://erichovde.com",
    "https://kamalaharris.com",
    "https://berniemoreno.com",    
    "https://erichovde.com",
    "https://kamalaharris.com",
    "https://berniemoreno.com",
    "https://erichovde.com",
    "https://kamalaharris.com",
    "https://berniemoreno.com",
]

def run_browser(profile_path, url):
    driver = create_driver(profile_path)
    driver.get(url)
    # Add your automation logic here
    print(f"Opened {url} in profile {profile_path}")
    driver.quit()
    
# Create and start threads
threads = []
for profile, url in zip(profiles, urls):
    thread = threading.Thread(target=run_browser, args=(profile, url))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()