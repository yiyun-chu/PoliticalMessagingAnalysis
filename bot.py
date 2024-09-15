import pandas as pd 
from driver_setup  import  create_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import  time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import json
driver = create_driver()
df = pd.read_csv("input.csv")
print(df['First Name'][0])
for i in  range(0,len(df['Url'])) :
        url = df['Url'][i]
        driver.get(url)
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
            all_form_input[0].send_keys(df['email'][i])
            all_form_input[1].send_keys("8755968766") 
            all_form_input[2].send_keys(int(df['zip'][i]))
            driver.find_element(By.XPATH,"//button[@type='submit']").click()
            time.sleep(6)
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')

            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            
            
        elif "karilake" in url:
            all_form_input[0].send_keys("john")
            all_form_input[1].send_keys("smit") 
            all_form_input[2].send_keys("8755968767")
            all_form_input[3].send_keys(df['email'][i])
            all_form_input[4].send_keys("delhi")  
            all_form_input[5].send_keys(int(df['zip'][i]))  
            submit = driver.find_element(By.XPATH,"//input[@type='submit']")
            driver.execute_script("arguments[0].click();",submit)
            time.sleep(10)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
            
        elif "elizabethwarren" in url: 
            all_form_input[0].send_keys(df['email'][i])
            all_form_input[1].send_keys(int(df['zip'][i]))
            all_form_input[2].send_keys("8755968766") 
            driver.find_element(By.XPATH,"//button[@type='submit']").click()
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
            
        elif "johndeatonforsenate" in url: 
            time.sleep(5)
            all_form_input[0].send_keys(df['First Name'][i])
            all_form_input[1].send_keys(df['Last Name'][i]) 
            all_form_input[2].send_keys(df['email'][i])
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
            
        elif "elissaslotkin.org" in url: 
            all_form_input[0].send_keys(df['email'][i])
            all_form_input[1].send_keys("8755968766") 
            all_form_input[2].send_keys(int(df['zip'][i]))
            driver.find_element(By.XPATH,"//button[@type='submit']").click()
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
            
        elif "rogersforsenate" in url: 
           all_form_input[0].send_keys(df['email'][i])
           all_form_input[1].send_keys("8755968766")
           all_form_input[2].send_keys(int(df['zip'][i]))
           driver.find_element(By.XPATH,"//button[@type='submit']").click()
           time.sleep(6)
        #    driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
           formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
           driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')
               
        elif "amyklobuchar" in  url: 
            all_form_input[0].send_keys(df['First Name'][i])
            all_form_input[1].send_keys(df['Last Name'][i]) 
            all_form_input[2].send_keys(int(df['zip'][i]))
            all_form_input[3].send_keys(df['email'][i]) 
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
            
        elif "roycewhite.us" in  url: 
            all_form_input[8].send_keys(df['First Name'][i])
            all_form_input[9].send_keys(df['Last Name'][i]) 
            all_form_input[10].send_keys(df['email'][i])
            all_form_input[11].send_keys("8755968766")  
            input = form.find_element(By.XPATH,"//input[@placeholder='ZIP Code*']")
            input.send_keys(int(df['zip'][i]))     
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
        elif "lucaskunce" in  url: 
            
            all_form_input[0].send_keys(df['First Name'][i])
            all_form_input[1].send_keys(df['Last Name'][i]) 
            all_form_input[2].send_keys(df['email'][i])
            all_form_input[3].send_keys(int(df['zip'][i]))   
            all_form_input[4].send_keys("8755968766")   
            submit = driver.find_element(By.XPATH,"//button[@type='submit']")
            driver.execute_script("arguments[0].click();",submit)
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
            
        elif "joshhawley" in  url:       
            driver.find_element(By.XPATH,"//input[@placeholder='First Name']").send_keys(df['First Name'][i])
            driver.find_element(By.XPATH,"//input[@placeholder='Last Name']").send_keys(df['Last Name'][i])
            driver.find_element(By.XPATH,"//input[@placeholder='Email Address']").send_keys(df['email'][i])
            driver.find_element(By.XPATH,"//input[@placeholder='Zip Code']").send_keys(int(df['zip'][i]))
            driver.find_element(By.XPATH,"//input[@placeholder='Phone Number (optional)']").send_keys("8755968766")
            submit = driver.find_element(By.XPATH,"//input[@type='submit']")
            driver.execute_script("arguments[0].click();",submit)
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
            
        elif "jontester" in url:          
    
            all_form_input[0].send_keys(df['email'][i])
            all_form_input[1].send_keys("8755968766") 
            all_form_input[2].send_keys(int(df['zip'][i]))
            submit = driver.find_element(By.XPATH,"//button[@type='submit']")
            driver.execute_script("arguments[0].click();", submit)
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
            
        elif "timformt" in url:
            all_form_input[0].send_keys(df['First Name'][i])
            all_form_input[1].send_keys(df['Last Name'][i]) 
            all_form_input[2].send_keys(df['email'][i])
            all_form_input[3].send_keys("8755968766")
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
            
        elif "rosenfornevada" in url:   
            time.sleep(3)
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.ESCAPE)
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@name='EmailAddress']").send_keys(df['email'][i])
            driver.find_element(By.XPATH,"//input[@name='MobilePhone']").send_keys("8755968766") 
            driver.find_element(By.XPATH,"//input[@name='PostalCode']").send_keys(int(df['zip'][i]))
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
            
        elif "secure.ngpvan.com" in url :
            
            all_form_input[0].send_keys(df['First Name'][i])
            all_form_input[1].send_keys(df['Last Name'][i]) 
            all_form_input[2].clear()
            all_form_input[2].send_keys(df['email'][i])
            all_form_input[3].clear()
            all_form_input[3].send_keys(int(df['zip'][i]))
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
        elif "captainsambrown" in url:   
            all_form_input[0].send_keys(df['email'][i])
            all_form_input[1].send_keys("8755968766") 
            all_form_input[2].send_keys(int(df['zip'][i]))
            driver.find_element(By.XPATH,"//input[@type='checkbox']").click()
            driver.find_element(By.XPATH,"//button[@type='submit']").click()
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
            
        elif "mikesapraiconeforsenate" in url:
            driver.find_element(By.XPATH,"//input[@placeholder='Cell Phone']").send_keys("8755968766")
            driver.find_element(By.XPATH,"//input[@placeholder='Email Address']").send_keys(df['email'][i]) 
            driver.find_element(By.XPATH,"//input[@placeholder='Zip Code']").send_keys(int(df['zip'][i]))
            driver.find_element(By.XPATH,"//button[@type='submit']").click()
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
            
        elif  "sherrodbrown" in url:
            time.sleep(3)
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.ESCAPE)
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@name='FirstName']").send_keys(df['First Name'][i])
            driver.find_element(By.XPATH,"//input[@name='LastName']").send_keys(df['Last Name'][i]) 
            driver.find_element(By.XPATH,"//input[@name='EmailAddress']").send_keys(df['email'][i])
            driver.find_element(By.XPATH,"//input[@name='MobilePhone']").send_keys("8755968766")
            driver.find_element(By.XPATH,"//input[@name='PostalCode']").send_keys(int(df['zip'][i]))
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
            
        elif "berniemoreno" in url:
        
            all_form_input[0].send_keys(df['First Name'][i])
            all_form_input[1].send_keys(df['Last Name'][i]) 
            all_form_input[2].send_keys(df['email'][i])
            all_form_input[3].send_keys("8755968766")
            driver.find_element(By.XPATH,"//button[@type='submit']").click()
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
            
        elif "bobcasey" in url:
            all_form_input[0].send_keys(df['First Name'][i])
            all_form_input[1].send_keys(df['Last Name'][i]) 
            all_form_input[2].send_keys(df['email'][i])
            all_form_input[3].send_keys(int(df['zip'][i]))
            all_form_input[4].send_keys("8755968766")
            submit = driver.find_element(By.XPATH,"//button[@type='submit']")
            driver.execute_script("arguments[0].click();", submit)
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
        elif "davemccormickpa" in url:
            all_form_input[0].send_keys(df['First Name'][i])
            all_form_input[1].send_keys(df['Last Name'][i]) 
            all_form_input[2].send_keys("8755968766")
            all_form_input[3].send_keys(int(df['zip'][i]))
            all_form_input[4].send_keys(df['email'][i])
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
            
        elif "votegloriajohnson"  in url :
            
            driver.find_element(By.XPATH,"//input[@placeholder='Email*']").send_keys(df['email'][i])
            driver.find_element(By.XPATH,"//input[@name='MobilePhone']").send_keys("8755968766") 
            driver.find_element(By.XPATH,"//input[@placeholder='ZIP Code*']").send_keys(int(df['zip'][i]))
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
            
        elif  "marshablackburn" in url:
            driver.find_element(By.XPATH,"//input[@placeholder='Email Address']").send_keys(df['email'][i]) 
            driver.find_element(By.XPATH,"//input[@placeholder='Zip Code']").send_keys(int(df['zip'][i]))
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
            
        elif "colinallred" in url:
            driver.find_element(By.XPATH,"//input[@placeholder='US Zip Code']").send_keys(int(df['zip'][i]))
            driver.find_element(By.XPATH,"//input[@placeholder='Email Address']").send_keys(df['email'][i])
            driver.find_element(By.XPATH,"//input[@placeholder='Phone']").send_keys("8755968766")
            driver.find_element(By.XPATH,"//button[@type='submit']").click()
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
            
        elif "erichovde" in url :
            all_form_input[0].send_keys(df['email'][i])
            all_form_input[1].send_keys(int(df['zip'][i])) 
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
        elif "kamalaharris" in url :
            try:
                driver.find_element(By.ID,"close-lightbox").click()
                time.sleep(1)
            except:
                pass
            driver.find_element(By.XPATH,"//input[@id='form-first_name']").send_keys(df['First Name'][i])
            driver.find_element(By.XPATH,"//input[@id='form-last_name']").send_keys(df['Last Name'][i]) 
            driver.find_element(By.XPATH,"//input[@id='form-email']").send_keys(df['email'][i])
            driver.find_element(By.XPATH,"//input[@id='form-zip_code']").send_keys(int(df['zip'][i]))
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')
        elif "tedcruz" in url:
            driver.find_element(By.XPATH,"//input[@placeholder='Email address*']").send_keys(df['email'][i])
            driver.find_element(By.XPATH,"//input[@placeholder='ZIP Code*']").send_keys(int(df['zip'][i]))
            driver.find_element(By.XPATH,"//input[@placeholder='Phone']").send_keys("8755968788")
            driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(12)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
        elif "tammybaldwin" in url:
            time.sleep(5)
            driver.find_element(By.XPATH,"//input[@placeholder='First name']").send_keys(df['First Name'][i])
            driver.find_element(By.XPATH,"//input[@placeholder='Last name']").send_keys(df['Last Name'][i])
            driver.find_element(By.XPATH,"//input[@placeholder='Email address*']").send_keys(df['email'][i])
            driver.find_element(By.XPATH,"//input[@placeholder='ZIP Code*']").send_keys(int(df['zip'][i]))
            driver.find_element(By.XPATH,"//input[@placeholder='Mobile phone']").send_keys("8755968766")
            driver.find_element(By.XPATH,"//button[@type='submit']").click()
            time.sleep(6)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')            
        elif "donaldjtrump"  in url:
            driver.find_element(By.XPATH,"//input[@placeholder='Enter your Email']").send_keys(df['email'][i])
            driver.find_element(By.XPATH,"//input[@placeholder='Zip']").send_keys(int(df['zip'][i]))
            driver.find_element(By.XPATH,"//input[@placeholder='Zip']").send_keys(Keys.ENTER)
            time.sleep(5)
            # driver.save_screenshot(f'{df['email'][i]+"_"+url.replace("www.","").split(".")[0].split("//")[1]}.png')
            formatted_url = url.replace("www.", "").split(".")[0].split("//")[1]
            driver.save_screenshot(f'{df["email"][i]}_{formatted_url}.png')        
        elif "berniemoreno" in url:
            pass