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

# Function to setup and return a Selenium WebDriver instance
# def create_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     user_data_dir = r"C:\Users\heinz_3\AppData\Local\Google\Chrome\User Data"
#     profile = "Profile 1"
#     chrome_options.add_argument(f"user-data-dir={user_data_dir}")
#     chrome_options.add_argument(f"profile-directory={profile}")


#     driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)
#     chrome_service = ChromeService(r'C:\Users\heinz_3\Downloads\election\chromedriver.exe')
#     return driver


def create_driver(profile_path):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-data-dir={profile_path}")
    if platform.system() == "Windows":
        chrome_service = ChromeService(executable_path=r'C:\Users\heinz_3\Downloads\election\chromedriver.exe')
    else:
        chrome_service = ChromeService(executable_path='/Users/athena/Desktop/Research/election/chromedriver-mac-arm64/chromedriver')
    return webdriver.Chrome(service=chrome_service, options=chrome_options)
