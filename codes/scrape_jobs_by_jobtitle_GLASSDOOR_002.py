from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import pandas as pd
import sys
from time import sleep
from datetime import datetime
from countdown import countdown

import pickle

def visit_glassdoor(driver,url):
    driver.get(url)

#def login(driver, login_frame,email_field, pw_field, signin_button, em, pw):
def login(driver,email_field, pw_field, signin_button, em, pw):

    wait = WebDriverWait(driver, 30)

    #try:
    #    login_iframe = driver.find_element_by_id(login_frame)
    #    driver.switch_to.frame(login_iframe)
    #except:
    #    print("Error locating iframe")

    try:            
        print(f"Locating email...", end= ' ')        
        email_visible = wait.until(EC.presence_of_element_located(email_field))
        print(f"Located successfully!")
        email_visible.send_keys(em)
        print("Email keyed in")
    except:        
        print("Error locating email or sending email")
        return False

    try:            
        print(f"Locating password...", end= ' ')

        #PASSWORD = (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div/div/div/div/div/div[1]/div[3]/form/div[2]/div/div/input")
        #PASSWORD_DIV = (By.CLASS_NAME, "mt-xsm")
        #password_div_visible = wait.until(EC.presence_of_element_located(password_div_visible))        
        password_visible = wait.until(EC.presence_of_element_located(pw_field))        

        print(f"Located successfully!")
        password_visible.send_keys(pw)

        password_visible.send_keys(Keys.ENTER)
        return True
        
    except:        
        print("Error locating password")
        return False        
    

def save_cookies():
        
    options = Options()
    options.add_argument("--window-size=1920,1200")
        
    DRIVER_PATH = 'c:\chromedriver\chromedriver.exe'                
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get("http://www.google.com")
    pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
    
    return driver


def restore_cookies():
    options = Options()
    options.add_argument("--window-size=1920,1200")
        
    DRIVER_PATH = 'c:\chromedriver\chromedriver.exe'                
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get("http://www.google.com")
    
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    return driver


def search_jobs(driver, keywords, keyword_element,button_element):

    wait = WebDriverWait(driver, 30)

    try:            
        print(f"Locating textfield to enter keywords...", end= ' ')
        textfield_visible = wait.until(EC.presence_of_element_located(keyword_element))
        print(f"Located successfully!")
        print(f"Sending {keywords} as keywords", end= ' ')
        textfield_visible.send_keys(keywords)        
    except:        
        print("Error locating the textfield")
        return False

    try:            
        print(f"Locating submit button ...", end= ' ')        
        button_visible = wait.until(EC.element_to_be_clickable(button_element))        
        print(f"Located successfully!")
        button_visible.click()

        return True

    except:        
        print("Error locating the submit button")        
        print(f"Error submitting job search to {websitename} with keywords {keywords}")
        for error in sys.exc_info():
            print(error)
        
        return False



if __name__ == "__main__":

    options = Options()
    options.add_argument("--window-size=1920,1200")
        
    DRIVER_PATH = 'c:\chromedriver\chromedriver.exe'                
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

    EMAIL_FIELD = (By.ID, 'userEmail')
    PASSWORD_FIELD = (By.ID, 'userPassword')
    #PASSWORD_FIELD = (By.CSS_SELECTOR, "input[type='submit']")
    #SIGNIN_BUTTON = (By.CSS_SELECTOR, "button.gd-ui-button minWidthBtn css-8i7bc2[type='submit']")
    SIGNIN_BUTTON = (By.CSS_SELECTOR, "input[type='submit']")

    GOOGLE_BUTTON = (By.CLASS_NAME, 'google gd-btn short')

    #KEYWORD_TEXTFIELD = (By.ID, "scKeyword")
    KEYWORD_TEXTFIELD = (By.CSS_SELECTOR,"input[data-test='search-menu-keyword-input']")
    BUTTON_SUBMIT = (By.CSS_SELECTOR, "button[data-test='search-bar-submit']")

    websitename = "Glassdoor"
    website_url = "https://www.glassdoor.sg/profile/login_input.htm"
    keywords = "data scientist"    
    
  
    try:                  
        #search_jobs(driver, websitename, website_url, keywords, KEYWORD_TEXTFIELD, BUTTON_SUBMIT)
        #driver = save_cookies()
        #driver = restore_cookies()
        visit_glassdoor(driver,website_url)
        login_successful = login(driver,EMAIL_FIELD,PASSWORD_FIELD,SIGNIN_BUTTON,"desiowprism55@gmail.com","dooRGD88!")

        print("Searching jobs")
        
        search_jobs(driver,keywords,KEYWORD_TEXTFIELD,BUTTON_SUBMIT)

    except:
        print(f"Error in main method")
        for error in sys.exc_info():
            print(error)                       

