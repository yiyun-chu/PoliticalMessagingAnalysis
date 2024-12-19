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

def create_driver(profile_path):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-data-dir={profile_path}")

    if platform.system() == "Windows":
        chrome_service = ChromeService(ChromeDriverManager().install())
    else:
        chrome_service = ChromeService(executable_path='CHROMEDRIVER_PATH')
        
    return webdriver.Chrome(service=chrome_service, options=chrome_options)
