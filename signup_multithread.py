import pandas as pd 
from driver_setup import create_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.common.keys import Keys
import platform
import os
import threading
from selenium.common.exceptions import WebDriverException
from vpn_automate import change_vpn, login_vpn
from selenium.common.exceptions import TimeoutException


if platform.system() == "Windows":
    save_dir = "YOUR_PATH"
    log_file = "YOUR_FILE_PATH"
else:
    save_dir = "YOUR_PATH"
    log_file = "YOUR_FILE_PATH"
        
with open('YOUR_VPN_LOGIN_CREDENTIALS.txt', 'r') as login_file:
    username = login_file.readline().strip()
    password = login_file.readline().strip()

df = pd.read_csv("YOUR_INPUT_DATA.csv")
login_vpn(username, password)
last_vpn = None

def process_row(row, profile_path):
    url = row['Url']
    profile_id = row['profile_id']

    driver = create_driver(profile_path)
    try:
        print(f"Opening: {url} for profile_id: {profile_id}")
        driver.get(url)
        time.sleep(2)
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.ESCAPE)
        time.sleep(1)
    
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
                    form = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.TAG_NAME, "form"))
                    )
                    break
                except TimeoutException:
                    print(f"Timeout on {url} for profile_id: {profile_id}")
                    return (profile_id, None, 0)
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
            all_form_input[0].send_keys(row['email'])
            time.sleep(1)
            all_form_input[1].send_keys("8755968766") 
            time.sleep(1)
            all_form_input[2].send_keys(int(row['zip']))
            time.sleep(1)
            driver.find_element(By.XPATH,"//button[@type='submit']").click()
            time.sleep(3)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)
            
            
        elif "karilake" in url:
            all_form_input[0].send_keys("john")
            time.sleep(1)
            all_form_input[1].send_keys("smit") 
            time.sleep(1)
            all_form_input[2].send_keys("8755968767")
            time.sleep(1)
            all_form_input[3].send_keys(row['email'])
            time.sleep(1)
            all_form_input[4].send_keys("delhi")
            time.sleep(1)  
            all_form_input[5].send_keys(int(row['zip']))
            time.sleep(1)  
            submit = driver.find_element(By.XPATH,"//input[@type='submit']")
            time.sleep(1)
            driver.execute_script("arguments[0].click();",submit)
            time.sleep(10)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)            
            
        elif "elizabethwarren" in url:
            all_form_input[0].send_keys(row['email'])
            time.sleep(1)
            all_form_input[1].send_keys(int(row['zip']))
            time.sleep(1)
            all_form_input[2].send_keys("8755968766")
            time.sleep(1) 
            driver.find_element(By.XPATH,"//button[@type='submit']").click()
            time.sleep(6)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)            
            
        elif "johndeatonforsenate" in url: 
            time.sleep(5)
            all_form_input[0].send_keys(row['First Name'])
            time.sleep(1)
            all_form_input[1].send_keys(row['Last Name'])
            time.sleep(1) 
            all_form_input[2].send_keys(row['email'])
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)            
            
        elif "elissaslotkin.org" in url:
            all_form_input[0].send_keys(row['email'])
            time.sleep(1)
            all_form_input[1].send_keys("8755968766")
            time.sleep(1) 
            all_form_input[2].send_keys(int(row['zip']))
            time.sleep(1)
            driver.find_element(By.XPATH,"//button[@type='submit']").click()
            time.sleep(6)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)            
            
        elif "rogersforsenate" in url:
            all_form_input[0].send_keys(row['email'])
            time.sleep(1)
            all_form_input[1].send_keys("8755968766")
            time.sleep(1)
            all_form_input[2].send_keys(int(row['zip']))
            driver.find_element(By.XPATH,"//button[@type='submit']").click()
            time.sleep(6)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)
                
        elif "amyklobuchar" in  url:
            all_form_input[0].send_keys(row['First Name'])
            time.sleep(1)
            all_form_input[1].send_keys(row['Last Name'])
            time.sleep(1) 
            all_form_input[2].send_keys(int(row['zip']))
            time.sleep(1)
            all_form_input[3].send_keys(row['email'])
            time.sleep(1) 
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)            
            
        elif "roycewhite.us" in  url:
            all_form_input[8].send_keys(row['First Name'])
            time.sleep(1)
            all_form_input[9].send_keys(row['Last Name'])
            time.sleep(1) 
            all_form_input[10].send_keys(row['email'])
            time.sleep(1)
            all_form_input[11].send_keys("8755968766")  
            time.sleep(1)
            input = form.find_element(By.XPATH,"//input[@placeholder='ZIP Code*']")
            time.sleep(1)
            input.send_keys(int(row['zip']))
            time.sleep(1)     
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)   
                        
        elif "lucaskunce" in  url:
            all_form_input[0].send_keys(row['First Name'])
            time.sleep(1)
            all_form_input[1].send_keys(row['Last Name'])
            time.sleep(1) 
            all_form_input[2].send_keys(row['email'])
            time.sleep(1)
            all_form_input[3].send_keys(int(row['zip']))
            time.sleep(1)   
            all_form_input[4].send_keys("8755968766")
            time.sleep(1)   
            submit = driver.find_element(By.XPATH,"//button[@type='submit']")
            time.sleep(6)
            driver.execute_script("arguments[0].click();",submit)
            time.sleep(6)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)            
            
        elif "joshhawley" in  url:
            driver.find_element(By.XPATH,"//input[@placeholder='First Name']").send_keys(row['First Name'])
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@placeholder='Last Name']").send_keys(row['Last Name'])
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@placeholder='Email Address']").send_keys(row['email'])
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@placeholder='Zip Code']").send_keys(int(row['zip']))
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@placeholder='Phone Number (optional)']").send_keys("8755968766")
            time.sleep(6)
            submit = driver.find_element(By.XPATH,"//input[@type='submit']")
            time.sleep(6)
            driver.execute_script("arguments[0].click();",submit)
            time.sleep(6)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)            
            
        elif "jontester" in url:
            all_form_input[0].send_keys(row['email'])
            time.sleep(1)
            all_form_input[1].send_keys("8755968766")
            time.sleep(1) 
            all_form_input[2].send_keys(int(row['zip']))
            time.sleep(1)
            submit = driver.find_element(By.XPATH,"//button[@type='submit']")
            time.sleep(6)

            driver.execute_script("arguments[0].click();", submit)
            time.sleep(6)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)            
            
        elif "timformt" in url:
            all_form_input[0].send_keys(row['First Name'])
            time.sleep(1)
            all_form_input[1].send_keys(row['Last Name'])
            time.sleep(1) 
            all_form_input[2].send_keys(row['email'])
            time.sleep(1)
            all_form_input[3].send_keys("8755968766")
            time.sleep(6)
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)            
            
        elif "rosenfornevada" in url:   
            time.sleep(3)
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.ESCAPE)
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@name='EmailAddress']").send_keys(row['email'])
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@name='MobilePhone']").send_keys("8755968766")
            time.sleep(1) 
            driver.find_element(By.XPATH,"//input[@name='PostalCode']").send_keys(int(row['zip']))
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)            
            
        elif "secure.ngpvan.com" in url :
            time.sleep(1)
            all_form_input[0].send_keys(row['First Name'])
            time.sleep(1)
            all_form_input[1].send_keys(row['Last Name'])
            time.sleep(1) 
            all_form_input[2].clear()
            time.sleep(1)
            all_form_input[2].send_keys(row['email'])
            time.sleep(1)
            all_form_input[3].clear()
            all_form_input[3].send_keys(int(row['zip']))
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_kirstengillibrand.png')
            driver.save_screenshot(screenshot_path)       

        elif "captainsambrown" in url:
            all_form_input[0].send_keys(row['email'])
            time.sleep(1)
            all_form_input[1].send_keys("8755968766")
            time.sleep(1) 
            all_form_input[2].send_keys(int(row['zip']))
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@type='checkbox']").click()
            time.sleep(1)
            driver.find_element(By.XPATH,"//button[@type='submit']").click()
            time.sleep(6)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)            
            
        elif "mikesapraiconeforsenate" in url:
            driver.find_element(By.XPATH,"//input[@placeholder='Cell Phone']").send_keys("8755968766")
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@placeholder='Email Address']").send_keys(row['email'])
            time.sleep(1) 
            driver.find_element(By.XPATH,"//input[@placeholder='Zip Code']").send_keys(int(row['zip']))
            time.sleep(1)
            driver.find_element(By.XPATH,"//button[@type='submit']").click()
            time.sleep(6)

            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)      
            
        elif  "sherrodbrown" in url:
            time.sleep(3)
            body = driver.find_element(By.TAG_NAME, 'body')
            time.sleep(1)
            body.send_keys(Keys.ESCAPE)
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@name='FirstName']").send_keys(row['First Name'])
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@name='LastName']").send_keys(row['Last Name'])
            time.sleep(1) 
            driver.find_element(By.XPATH,"//input[@name='EmailAddress']").send_keys(row['email'])
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@name='MobilePhone']").send_keys("8755968766")
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@name='PostalCode']").send_keys(int(row['zip']))
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)            
            
        elif "berniemoreno" in url:
            time.sleep(3)
            all_form_input[0].send_keys(row['First Name'])
            time.sleep(1)
            all_form_input[1].send_keys(row['Last Name']) 
            time.sleep(1)
            all_form_input[2].send_keys(row['email'])
            time.sleep(1)
            all_form_input[3].send_keys("8755968766")
            time.sleep(1)
            driver.find_element(By.XPATH,"//button[@type='submit']").click()
            time.sleep(1)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)            
            
        elif "bobcasey" in url:
            time.sleep(2)
            all_form_input[0].send_keys(row['First Name'])
            time.sleep(1)
            all_form_input[1].send_keys(row['Last Name'])
            time.sleep(1) 
            all_form_input[2].send_keys(row['email'])
            time.sleep(1)
            all_form_input[3].send_keys(int(row['zip']))
            time.sleep(1)
            all_form_input[4].send_keys("8755968766")
            time.sleep(1)
            submit = driver.find_element(By.XPATH,"//button[@type='submit']")
            driver.execute_script("arguments[0].click();", submit)
            time.sleep(10)
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)
                        
        elif "davemccormickpa" in url:
            time.sleep(1)
            all_form_input[0].send_keys(row['First Name'])
            time.sleep(1)
            all_form_input[1].send_keys(row['Last Name'])
            time.sleep(1) 
            all_form_input[2].send_keys("8755968766")
            time.sleep(1)
            all_form_input[3].send_keys(int(row['zip']))
            time.sleep(1)
            all_form_input[4].send_keys(row['email'])
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)            
            
        elif "votegloriajohnson"  in url :
            driver.find_element(By.XPATH,"//input[@placeholder='Email*']").send_keys(row['email'])
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@name='MobilePhone']").send_keys("8755968766")
            time.sleep(1) 
            driver.find_element(By.XPATH,"//input[@placeholder='ZIP Code*']").send_keys(int(row['zip']))
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)            
            
        elif "marshablackburn" in url:
            driver.find_element(By.XPATH,"//input[@placeholder='Email Address']").send_keys(row['email'])
            time.sleep(1) 
            driver.find_element(By.XPATH,"//input[@placeholder='Zip Code']").send_keys(int(row['zip']))
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)            
            
        elif "colinallred" in url:
            driver.find_element(By.XPATH,"//input[@placeholder='US Zip Code']").send_keys(int(row['zip']))
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@placeholder='Email Address']").send_keys(row['email'])
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@placeholder='Phone']").send_keys("8755968766")
            time.sleep(1)
            driver.find_element(By.XPATH,"//button[@type='submit']").click()
            time.sleep(6)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)            
            
        elif "erichovde" in url :
            all_form_input[0].send_keys(row['email'])
            time.sleep(1)
            all_form_input[1].send_keys(int(row['zip'])) 
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)            
            
        elif "kamalaharris" in url :
            try:
                driver.find_element(By.ID,"close-lightbox").click()
                time.sleep(1)
            except:
                pass
            driver.find_element(By.XPATH,"//input[@id='form-first_name']").send_keys(row['First Name'])
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@id='form-last_name']").send_keys(row['Last Name'])
            time.sleep(1) 
            driver.find_element(By.XPATH,"//input[@id='form-email']").send_keys(row['email'])
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@id='form-zip_code']").send_keys(int(row['zip']))
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)
            
        elif "tedcruz" in url:
            time.sleep(15)
            driver.find_element(By.XPATH,"//input[@placeholder='Email address*']").send_keys(row['email'])
            time.sleep(2)
            driver.find_element(By.XPATH,"//input[@placeholder='ZIP Code*']").send_keys(int(row['zip']))
            time.sleep(2)
            driver.find_element(By.XPATH,"//input[@placeholder='Phone']").send_keys("8755968788")
            time.sleep(2)
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(20)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)            
            
        elif "tammybaldwin" in url:
            time.sleep(5)
            driver.find_element(By.XPATH,"//input[@placeholder='First name']").send_keys(row['First Name'])
            time.sleep(5)
            driver.find_element(By.XPATH,"//input[@placeholder='Last name']").send_keys(row['Last Name'])
            time.sleep(5)
            driver.find_element(By.XPATH,"//input[@placeholder='Email address*']").send_keys(row['email'])
            time.sleep(5)
            driver.find_element(By.XPATH,"//input[@placeholder='ZIP Code*']").send_keys(int(row['zip']))
            time.sleep(5)
            driver.find_element(By.XPATH,"//input[@placeholder='Mobile phone']").send_keys("8755968766")
            time.sleep(6)
            driver.find_element(By.XPATH,"//button[@type='submit']").click()
            time.sleep(6)
            
            username = row["email"].split("@")[0]
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
            driver.save_screenshot(screenshot_path)            
            
        elif "donaldjtrump"  in url:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your Email']"))
                )
                driver.find_element(By.XPATH,"//input[@placeholder='Enter your Email']").send_keys(row['email'])
                time.sleep(1)
                driver.find_element(By.XPATH,"//input[@placeholder='Zip']").send_keys(int(row['zip']))
                time.sleep(1)
                driver.find_element(By.XPATH,"//input[@placeholder='Zip']").send_keys(Keys.ENTER)
                time.sleep(5)
                
                username = row["email"].split("@")[0]
                formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
                screenshot_path = os.path.join(save_dir, f'{username}_{formatted_url}.png')
                driver.save_screenshot(screenshot_path)        
                
            except TimeoutException:
                print(f"Timeout on form submission for profile_id: {profile_id}")
                return (profile_id, None, f"Timeout on form submission for profile_id: {profile_id}")
            
        return (profile_id, screenshot_path, 1)
    
    except WebDriverException as e:
        print(f"Error processing profile_id: {profile_id}: {e}")
        return (profile_id, None, f"Error processing profile_id: {profile_id}: {e}")
    
    finally:
        driver.quit()

def process_vpn_region(region_df, profile_paths):
    pia_vpn = region_df['pia_vpn'].iloc[0]
    vpn_ip = change_vpn(pia_vpn)
    if not vpn_ip:
        print(f"Failed to connect to VPN for {pia_vpn}")
        return []

    threads = []
    results = []
    
    def thread_target(profile_path, row):
        result = process_row(row, profile_path)
        results.append(result)

    rows_to_process = region_df.head(len(profile_paths))
    for (_, row), profile_path in zip(rows_to_process.iterrows(), profile_paths):
        thread = threading.Thread(target=thread_target, args=(profile_path, row))
        threads.append(thread)
        thread.start()
        
    for thread in threads:
        thread.join()

    return results

def run_vpn_region_based():
    grouped = df.groupby('pia_vpn')
    
    all_results = []
    
    profiles = ['YOUR_PROFILES']

    for pia_vpn, group in grouped:
        print(f"Processing region: {pia_vpn}")
        results = process_vpn_region(group, profiles)
        all_results.extend(results)
    
    with open(log_file, 'a') as f:
        for result in all_results:
            if result:
                f.write(f'{result[0]},{result[1]},{result[2]}\n')

run_vpn_region_based()