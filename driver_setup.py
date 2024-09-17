import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests
import time
import pandas as pd 
from urllib.parse import urlparse
import platform
data_list = []

def create_driver(profile_path):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"user-data-dir={profile_path}")

    if platform.system() == "Windows":
        # chrome_service = ChromeService(executable_path=r'C:\Users\Heinz1\Documents\chromedriver.exe')
        chrome_service = ChromeService(ChromeDriverManager().install())
        # chrome_service = ChromeService(ChromeDriverManager(cache_valid_range=0).install())

    else:
        chrome_service = ChromeService(executable_path='/Users/athena/Desktop/Research/election/chromedriver-mac-arm64/chromedriver')
    return webdriver.Chrome(service=chrome_service, options=chrome_options)
