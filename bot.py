import pandas as pd 
from driver_setup import create_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import json
import os

import concurrent.futures
from selenium.common.exceptions import WebDriverException
from vpn_automate import change_vpn, login_vpn

save_dir = r"C:\Users\heinz_3\Dropbox\after_submit_screenshot"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
    
driver = create_driver()
df = pd.read_csv("test.csv")

with open('login.txt', 'r') as login_file:
    username = login_file.readline().strip()
    password = login_file.readline().strip()

# Log in to the VPN
login_vpn(username, password)
last_vpn = None

for i in range(len(df['Url'])):
    url = df['Url'][i]
    pia_vpn = df['pia_vpn'][i]

    # Change VPN if necessary
    if pia_vpn != last_vpn:
        vpn_ip = change_vpn(pia_vpn)
        if vpn_ip:
            last_vpn = pia_vpn  
            df.at[i, 'VPN_IP'] = vpn_ip
            df.at[i, 'Profile'] = pia_vpn
        else:
            print(f"Failed to connect to VPN for {pia_vpn}")
            continue

    driver.get(url)
    time.sleep(2)
    driver.maximize_window()
    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.ESCAPE)
    time.sleep(1)
    # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
    
    if "elizabethwarren" in url:
        form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )
        driver.find_element(By.XPATH,"//a[@class='Blocks__ContinueCTA-sc-1j0jrdb-26 fbTNUG']").click()
    
    elif "jontester" in url:
        driver.find_element(By.XPATH,"//button[@aria-label='close popup']").click()
        form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )
    
    elif "colinallred"   in url:  
        try:
            driver.find_element(By.XPATH,"//a[@class='modal1-close icon-close']").click()
            time.sleep(1)
            form = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
        except:
            form = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            
    elif "donaldjtrump" in url:
        while True:
            try:
                close_popup = driver.find_element(By.XPATH,"//button[@aria-label='Close Popup']")
                driver.execute_script("arguments[0].click();", close_popup)
                time.sleep(1)
                form = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "form"))
                )
                break
            except:
                pass
            
    else:
        form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )
    all_form_input = form.find_elements(By.TAG_NAME,"input")
    
    try:
        WebDriverWait(driver, 10).until(
                    EC.visibility_of(all_form_input[0]))
    except:
        pass
        
    if "gallegoforarizona" in url:
        time.sleep(1)
        all_form_input[0].send_keys(df['email'][i])
        time.sleep(1)
        all_form_input[1].send_keys("8755968766") 
        time.sleep(1)
        all_form_input[2].send_keys(int(df['zip'][i]))
        time.sleep(1)
        driver.find_element(By.XPATH,"//button[@type='submit']").click()
        time.sleep(3)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)
        
        
    elif "karilake" in url:
        time.sleep(1)
        all_form_input[0].send_keys("john")
        time.sleep(1)
        all_form_input[1].send_keys("smit") 
        time.sleep(1)
        all_form_input[2].send_keys("8755968767")
        time.sleep(1)
        all_form_input[3].send_keys(df['email'][i])
        time.sleep(1)
        all_form_input[4].send_keys("delhi")
        time.sleep(1)  
        all_form_input[5].send_keys(int(df['zip'][i]))
        time.sleep(1)  
        submit = driver.find_element(By.XPATH,"//input[@type='submit']")
        time.sleep(1)
        driver.execute_script("arguments[0].click();",submit)
        time.sleep(10)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)            
        
    elif "elizabethwarren" in url:
        time.sleep(6) 
        all_form_input[0].send_keys(df['email'][i])
        time.sleep(1)
        all_form_input[1].send_keys(int(df['zip'][i]))
        time.sleep(1)
        all_form_input[2].send_keys("8755968766")
        time.sleep(1) 
        driver.find_element(By.XPATH,"//button[@type='submit']").click()
        time.sleep(6)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)            
        
    elif "johndeatonforsenate" in url: 
        time.sleep(5)
        all_form_input[0].send_keys(df['First Name'][i])
        time.sleep(1)
        all_form_input[1].send_keys(df['Last Name'][i])
        time.sleep(1) 
        all_form_input[2].send_keys(df['email'][i])
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@type='submit']").click()
        time.sleep(6)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)            
        
    elif "elissaslotkin.org" in url:
        time.sleep(1) 
        all_form_input[0].send_keys(df['email'][i])
        time.sleep(1)
        all_form_input[1].send_keys("8755968766")
        time.sleep(1) 
        all_form_input[2].send_keys(int(df['zip'][i]))
        time.sleep(1)
        driver.find_element(By.XPATH,"//button[@type='submit']").click()
        time.sleep(6)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)            
        
    elif "rogersforsenate" in url:
        time.sleep(1) 
        all_form_input[0].send_keys(df['email'][i])
        time.sleep(1)
        all_form_input[1].send_keys("8755968766")
        time.sleep(1)
        all_form_input[2].send_keys(int(df['zip'][i]))
        driver.find_element(By.XPATH,"//button[@type='submit']").click()
        time.sleep(6)
        
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)
            
    elif "amyklobuchar" in  url:
        time.sleep(1) 
        all_form_input[0].send_keys(df['First Name'][i])
        time.sleep(1)
        all_form_input[1].send_keys(df['Last Name'][i])
        time.sleep(1) 
        all_form_input[2].send_keys(int(df['zip'][i]))
        time.sleep(1)
        all_form_input[3].send_keys(df['email'][i])
        time.sleep(1) 
        driver.find_element(By.XPATH,"//input[@type='submit']").click()
        time.sleep(6)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)            
        
    elif "roycewhite.us" in  url:
        time.sleep(1) 
        all_form_input[8].send_keys(df['First Name'][i])
        time.sleep(1)
        all_form_input[9].send_keys(df['Last Name'][i])
        time.sleep(1) 
        all_form_input[10].send_keys(df['email'][i])
        time.sleep(1)
        all_form_input[11].send_keys("8755968766")  
        time.sleep(1)
        input = form.find_element(By.XPATH,"//input[@placeholder='ZIP Code*']")
        time.sleep(1)
        input.send_keys(int(df['zip'][i]))
        time.sleep(1)     
        driver.find_element(By.XPATH,"//input[@type='submit']").click()
        time.sleep(6)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)   
                    
    elif "lucaskunce" in  url:
        time.sleep(1) 
        all_form_input[0].send_keys(df['First Name'][i])
        time.sleep(1)
        all_form_input[1].send_keys(df['Last Name'][i])
        time.sleep(1) 
        all_form_input[2].send_keys(df['email'][i])
        time.sleep(1)
        all_form_input[3].send_keys(int(df['zip'][i]))
        time.sleep(1)   
        all_form_input[4].send_keys("8755968766")
        time.sleep(1)   
        submit = driver.find_element(By.XPATH,"//button[@type='submit']")
        time.sleep(6)
        driver.execute_script("arguments[0].click();",submit)
        time.sleep(6)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)            
        
    elif "joshhawley" in  url:
        time.sleep(1)       
        driver.find_element(By.XPATH,"//input[@placeholder='First Name']").send_keys(df['First Name'][i])
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@placeholder='Last Name']").send_keys(df['Last Name'][i])
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@placeholder='Email Address']").send_keys(df['email'][i])
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@placeholder='Zip Code']").send_keys(int(df['zip'][i]))
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@placeholder='Phone Number (optional)']").send_keys("8755968766")
        time.sleep(6)
        submit = driver.find_element(By.XPATH,"//input[@type='submit']")
        time.sleep(6)
        driver.execute_script("arguments[0].click();",submit)
        time.sleep(6)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)            
        
    elif "jontester" in url:
        time.sleep(1)          
        all_form_input[0].send_keys(df['email'][i])
        time.sleep(1)
        all_form_input[1].send_keys("8755968766")
        time.sleep(1) 
        all_form_input[2].send_keys(int(df['zip'][i]))
        time.sleep(1)
        submit = driver.find_element(By.XPATH,"//button[@type='submit']")
        time.sleep(6)

        driver.execute_script("arguments[0].click();", submit)
        time.sleep(6)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)            
        
    elif "timformt" in url:
        all_form_input[0].send_keys(df['First Name'][i])
        time.sleep(1)
        all_form_input[1].send_keys(df['Last Name'][i])
        time.sleep(1) 
        all_form_input[2].send_keys(df['email'][i])
        time.sleep(1)
        all_form_input[3].send_keys("8755968766")
        time.sleep(6)
        driver.find_element(By.XPATH,"//input[@type='submit']").click()
        time.sleep(6)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)            
        
    elif "rosenfornevada" in url:   
        time.sleep(3)
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.ESCAPE)
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@name='EmailAddress']").send_keys(df['email'][i])
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@name='MobilePhone']").send_keys("8755968766")
        time.sleep(1) 
        driver.find_element(By.XPATH,"//input[@name='PostalCode']").send_keys(int(df['zip'][i]))
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@type='submit']").click()
        time.sleep(6)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)            
        
    elif "secure.ngpvan.com" in url :
        time.sleep(1)
        all_form_input[0].send_keys(df['First Name'][i])
        time.sleep(1)
        all_form_input[1].send_keys(df['Last Name'][i])
        time.sleep(1) 
        all_form_input[2].clear()
        time.sleep(1)
        all_form_input[2].send_keys(df['email'][i])
        time.sleep(1)
        all_form_input[3].clear()
        all_form_input[3].send_keys(int(df['zip'][i]))
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@type='submit']").click()
        time.sleep(6)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)       

    elif "captainsambrown" in url:
        time.sleep(1)   
        all_form_input[0].send_keys(df['email'][i])
        time.sleep(1)
        all_form_input[1].send_keys("8755968766")
        time.sleep(1) 
        all_form_input[2].send_keys(int(df['zip'][i]))
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@type='checkbox']").click()
        time.sleep(1)
        driver.find_element(By.XPATH,"//button[@type='submit']").click()
        time.sleep(6)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)            
        
    elif "mikesapraiconeforsenate" in url:
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@placeholder='Cell Phone']").send_keys("8755968766")
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@placeholder='Email Address']").send_keys(df['email'][i])
        time.sleep(1) 
        driver.find_element(By.XPATH,"//input[@placeholder='Zip Code']").send_keys(int(df['zip'][i]))
        time.sleep(1)
        driver.find_element(By.XPATH,"//button[@type='submit']").click()
        time.sleep(6)

        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_kirstengillibrano.png')
        driver.save_screenshot(screenshot_path)      
        
    elif  "sherrodbrown" in url:
        time.sleep(3)
        body = driver.find_element(By.TAG_NAME, 'body')
        time.sleep(1)
        body.send_keys(Keys.ESCAPE)
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@name='FirstName']").send_keys(df['First Name'][i])
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@name='LastName']").send_keys(df['Last Name'][i])
        time.sleep(1) 
        driver.find_element(By.XPATH,"//input[@name='EmailAddress']").send_keys(df['email'][i])
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@name='MobilePhone']").send_keys("8755968766")
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@name='PostalCode']").send_keys(int(df['zip'][i]))
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@type='submit']").click()
        time.sleep(6)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)            
        
    elif "berniemoreno" in url:
        time.sleep(6)
        all_form_input[0].send_keys(df['First Name'][i])
        time.sleep(6)
        all_form_input[1].send_keys(df['Last Name'][i]) 
        time.sleep(6)
        all_form_input[2].send_keys(df['email'][i])
        time.sleep(6)
        all_form_input[3].send_keys("8755968766")
        time.sleep(6)
        driver.find_element(By.XPATH,"//button[@type='submit']").click()
        time.sleep(6)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)            
        
    elif "bobcasey" in url:
        time.sleep(1)
        all_form_input[0].send_keys(df['First Name'][i])
        time.sleep(1)
        all_form_input[1].send_keys(df['Last Name'][i])
        time.sleep(1) 
        all_form_input[2].send_keys(df['email'][i])
        time.sleep(1)
        all_form_input[3].send_keys(int(df['zip'][i]))
        time.sleep(1)
        all_form_input[4].send_keys("8755968766")
        time.sleep(1)
        submit = driver.find_element(By.XPATH,"//button[@type='submit']")
        driver.execute_script("arguments[0].click();", submit)
        time.sleep(6)
        
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)
                    
    elif "davemccormickpa" in url:
        time.sleep(1)
        all_form_input[0].send_keys(df['First Name'][i])
        time.sleep(1)
        all_form_input[1].send_keys(df['Last Name'][i])
        time.sleep(1) 
        all_form_input[2].send_keys("8755968766")
        time.sleep(1)
        all_form_input[3].send_keys(int(df['zip'][i]))
        time.sleep(1)
        all_form_input[4].send_keys(df['email'][i])
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@type='submit']").click()
        time.sleep(6)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)            
        
    elif "votegloriajohnson"  in url :
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@placeholder='Email*']").send_keys(df['email'][i])
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@name='MobilePhone']").send_keys("8755968766")
        time.sleep(1) 
        driver.find_element(By.XPATH,"//input[@placeholder='ZIP Code*']").send_keys(int(df['zip'][i]))
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@type='submit']").click()
        time.sleep(6)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)            
        
    elif  "marshablackburn" in url:
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@placeholder='Email Address']").send_keys(df['email'][i])
        time.sleep(1) 
        driver.find_element(By.XPATH,"//input[@placeholder='Zip Code']").send_keys(int(df['zip'][i]))
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@type='submit']").click()
        time.sleep(6)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)            
        
    elif "colinallred" in url:
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@placeholder='US Zip Code']").send_keys(int(df['zip'][i]))
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@placeholder='Email Address']").send_keys(df['email'][i])
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@placeholder='Phone']").send_keys("8755968766")
        time.sleep(1)
        driver.find_element(By.XPATH,"//button[@type='submit']").click()
        time.sleep(6)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)            
        
    elif "erichovde" in url :
        time.sleep(1)
        all_form_input[0].send_keys(df['email'][i])
        time.sleep(1)
        all_form_input[1].send_keys(int(df['zip'][i])) 
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@type='submit']").click()
        time.sleep(6)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)            
        
    elif "kamalaharris" in url :
        try:
            driver.find_element(By.ID,"close-lightbox").click()
            time.sleep(1)
        except:
            pass
        driver.find_element(By.XPATH,"//input[@id='form-first_name']").send_keys(df['First Name'][i])
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@id='form-last_name']").send_keys(df['Last Name'][i])
        time.sleep(1) 
        driver.find_element(By.XPATH,"//input[@id='form-email']").send_keys(df['email'][i])
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@id='form-zip_code']").send_keys(int(df['zip'][i]))
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@type='submit']").click()
        time.sleep(6)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)
        
    elif "tedcruz" in url:
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@placeholder='Email address*']").send_keys(df['email'][i])
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@placeholder='ZIP Code*']").send_keys(int(df['zip'][i]))
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@placeholder='Phone']").send_keys("8755968788")
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@type='submit']").click()
        time.sleep(12)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)            
        
    elif "tammybaldwin" in url:
        time.sleep(5)
        driver.find_element(By.XPATH,"//input[@placeholder='First name']").send_keys(df['First Name'][i])
        time.sleep(5)
        driver.find_element(By.XPATH,"//input[@placeholder='Last name']").send_keys(df['Last Name'][i])
        time.sleep(5)
        driver.find_element(By.XPATH,"//input[@placeholder='Email address*']").send_keys(df['email'][i])
        time.sleep(5)
        driver.find_element(By.XPATH,"//input[@placeholder='ZIP Code*']").send_keys(int(df['zip'][i]))
        time.sleep(5)
        driver.find_element(By.XPATH,"//input[@placeholder='Mobile phone']").send_keys("8755968766")
        time.sleep(6)
        driver.find_element(By.XPATH,"//button[@type='submit']").click()
        time.sleep(6)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)            
        
    elif "donaldjtrump"  in url:
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@placeholder='Enter your Email']").send_keys(df['email'][i])
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@placeholder='Zip']").send_keys(int(df['zip'][i]))
        time.sleep(1)
        driver.find_element(By.XPATH,"//input[@placeholder='Zip']").send_keys(Keys.ENTER)
        time.sleep(5)
        
        username = df["email"][i].split("@")[0]
        formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
        screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
        driver.save_screenshot(screenshot_path)        

    # df.to_csv('input.csv')

driver.quit()