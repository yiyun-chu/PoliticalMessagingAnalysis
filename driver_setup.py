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

data_list = []

# Function to setup and return a Selenium WebDriver instance
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    user_data_dir = r"C:\Users\heinz_3\AppData\Local\Google\Chrome\User Data"
    profile = "Profile 1"
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"profile-directory={profile}")

    chrome_options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"  # Update this path if needed

    # driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)
    chrome_service = ChromeService(r'C:\Users\heinz_3\Downloads\election\chromedriver.exe')
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return driver
