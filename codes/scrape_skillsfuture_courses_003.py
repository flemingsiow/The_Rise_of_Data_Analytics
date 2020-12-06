from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import sys
from time import sleep
from datetime import datetime
from countdown import countdown

import pickle

# https://www.myskillsfuture.sg/content/portal/en/training-exchange/course-directory.html
# ?fq=Course_Supp_Period_To_1%3A%5B2020-11-28T00%3A00%3A00Z%20TO%20*%5D&fq=IsValid%3Atrue&q=data%20governance&start=21&autocomplete=true#

#https://www.myskillsfuture.sg/content/portal/en/training-exchange/course-directory.html&q=data%20governance

def visit_skillsfuture(driver,url):
    driver.get(url)

def locate_element(wait, element_name, element_by):
    try:            
        print(f"Locating {element_name}")
        element_visible = wait.until(EC.presence_of_element_located(element_by))
        print(f"Located successfully!")            
        return True, element_visible
    except:        
        print(f"Error locating {element_name}")
        return False, element_visible

def click_load_all_button():

    wait = WebDriverWait(driver, 30)

    try:           
        # driver.find_elements_by_xpath("//*[contains(text(), 'Load More')]")                     
        load_more_button = wait.until(EC.element_to_be_clickable(LOAD_MORE))
        print("Found the load_more button")
        return True, load_more_button
        
    except:
        print("Could not locate the load_more button")
        return False, None

def load_all(driver,num_cards_to_load):

    load_more_button_present,load_more_button = click_load_all_button()
    num_cards_loaded, course_cards = get_course_cards()
    print(f"{num_cards_loaded} cards loaded...")

    while load_more_button_present and num_cards_loaded< num_cards_to_load:
        print("Clicked the load more button")
        load_more_button.click()
        load_more_button_present,load_more_button = click_load_all_button()
        num_cards_loaded, course_cards = get_course_cards()
        print(f"{num_cards_loaded} cards loaded...")

    return num_cards_loaded, course_cards

def get_course_cards():    
    course_cards = driver.find_elements_by_class_name("card")
    return len(course_cards), course_cards
    
def scrape_courses(driver,courses,number_of_courses):
    
    wait = WebDriverWait(driver, 30)

    try:

        total_courses = wait.until(EC.presence_of_element_located(TOTAL_RECORD))
        print(total_courses.text)

    except:
        print("Could not locate course total")
        for err in sys.exc_info():
            print(err)
        return False

    try:
        num_cards_loaded, course_cards = load_all(driver,number_of_courses)
    except:
        print("Could not load more")
        for err in sys.exc_info():
            print(err)
        return False

    try:
        print("Retrieving course information...")
        get_course_card_info(driver,courses, course_cards)
        print("Course information retrieved!")
        return True

    except:
        print("Could not retrieve information from course cards")
        for err in sys.exc_info():
            print(err)
        return False

# https://stackoverflow.com/questions/3939361/remove-specific-characters-from-a-string-in-python
def remove_chars(original_string):
    line = filter(lambda char: char not in "$?.!/;:", original_string)
    return line

def get_course_details(url,course):
    
    options = Options()
    options.add_argument("--window-size=1920,1200")
        
    DRIVER_PATH = 'c:\chromedriver\chromedriver.exe'                
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    wait = WebDriverWait(driver, 30)

    try:            
        driver.get(url)
        
    except:
        print(f"Could not load {url}")
        for err in sys.exc_info():
            print(err)
        return False        

    try:
        # courseDetail.courseTitle
        full_course_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-bind="text : courseDetail.courseTitle"')))                        
        full_course_objectives = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p[data-bind="html : courseDetail.courseObjective"')))
        full_course_content = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p[data-bind="html : courseDetail.courseContent"')))
        return full_course_title.text, full_course_objectives.text, full_course_content.text

    except:
        print(f"Error while fetching course details for {course['title_header']}")
        for err in sys.exc_info():
            print(err)
        return "", ""

    finally:
        driver.quit()


def get_course_card_info(driver,courses,course_cards):

    for i in range(0,len(course_cards)):
        try:
            course = {}
            element = course_cards[i]

            course_title_header = element.find_element(By.CLASS_NAME,  COURSE_TITLE_PARAM)
            course_provider = element.find_element(By.CLASS_NAME, COURSE_PROVIDER_PARAM)
            course_fee = element.find_element(By.CLASS_NAME, COURSE_FEES_PARAM)    
            course_refnum = element.find_element(By.XPATH, COURSE_REFNUM_PARAM)    
            course_link = course_title_header.find_element(By.TAG_NAME, "a")
            course_link_text = course_link.get_attribute('href')            
                    
            course['title_header'] = course_title_header.text
            course['company'] = course_provider.text
            course['fee'] = str(course_fee.text).replace("$","").replace(",","")
            course['link'] = course_link_text
            course['refnum'] = course_refnum.text

            course_title,course_objectives,course_content = get_course_details(course_link_text, course)

            course['full_course_title'] = course_title
            course['course_objectives'] = course_objectives
            course['course_content'] = course_content

            courses.append(course)

        except NoSuchElementException as e:
            for err in sys.exc_info():  
                print(err)
            continue
            
        except:
            print(f"Error retrieving information for course {i}")
            for err in sys.exc_info():
                print(err)
            continue

def save_courses(courses, filename):
    df = pd.DataFrame(courses)
    df.to_excel(filename)

if __name__ == "__main__":

    options = Options()
    options.add_argument("--window-size=1920,1200")
        
    DRIVER_PATH = 'c:\chromedriver\chromedriver.exe'                
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    
    KEYWORD_TEXTFIELD = (By.ID,"inputlg")
    BUTTON_SUBMIT = (By.CSS_SELECTOR, "button[class='searchSubmit']")

    COURSE_TITLE_PARAM = "coursetitle"
    COURSE_PROVIDER_PARAM = "school"
    COURSE_FEES_PARAM = "feefigure"
    COURSE_REFNUM_PARAM = "//span[@data-bind='html: EXT_Course_Ref_Nos[0]']"
    
    # https://stackoverflow.com/questions/42245745/selenium-python-multiple-classes-in-an-xpath-statement/42246035
    COURSE_CARD = (By.XPATH,"//div[contains(@class, 'card') and contains(@class, 'medium')]")
    COURSE_TITLE = (By.CLASS_NAME,COURSE_TITLE_PARAM)
    COURSE_REFNUM = (By.XPATH,"//span[contains[@data-bind,'html: EXT_Course_Ref_Nos']")
    COURSE_PROVIDER = (By.CLASS_NAME, COURSE_PROVIDER_PARAM)
    COURSE_FEES = (By.CLASS_NAME, COURSE_FEES_PARAM)
    LOAD_MORE = (By.XPATH, "//button[contains(text(), 'Load')]")
    TOTAL_RECORD = (By.ID, "totalRecord") 

    websitename = "Skills Future"
    keywords = "machine learning"  
    website_url = f"https://www.myskillsfuture.sg/content/portal/en/training-exchange/course-directory.html?fq=IsValid%3Atrue&q={keywords}"
    
    courses = []

    num_courses_to_scrape = 30

    try:                  
        
        print("Searching courses")
        visit_skillsfuture(driver,website_url)
        scrape_courses(driver,courses, num_courses_to_scrape)
        print(f"{len(courses)} found")
        save_courses(courses,"skillsfuture_courses_machine_learning.xlsx")

    except:
        print(f"Error in main method")
        for error in sys.exc_info():
            print(error)                       

