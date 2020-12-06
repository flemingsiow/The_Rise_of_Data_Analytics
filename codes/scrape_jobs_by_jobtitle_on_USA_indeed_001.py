from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement 
from selenium.common.exceptions import NoSuchElementException

from fake_useragent import UserAgent

import pandas as pd
import sys
from time import sleep
from datetime import datetime

# define the countdown func. 
def countdown(t): 

    # import the time module 
    import time 

    while t: 
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        #print(timer, end="\r") 
        print(timer)
        time.sleep(1) 
        t -= 1
    

def get_average_salary(salary):
    
    average_salary = 0

    salary = salary.replace("$","")
    salary = salary.replace(",","")
    salary = salary.replace(" ","")

    print(f"Salary is {salary}")

    
    try:

        if salary.find("-") == -1:
            lower_limit_start_index = 0
            lower_limit_end_index = salary.find("a")
            lower_limit_salary = salary[lower_limit_start_index:lower_limit_end_index]
            return lower_limit_salary, lower_limit_salary, lower_limit_salary
        else:
            #2000 - 8000 a month
            lower_limit_start_index = 0
            lower_limit_end_index = salary.find("-")
            #print(lower_limit_start_index)
            #print(lower_limit_end_index)
            lower_limit_salary = salary[lower_limit_start_index:lower_limit_end_index]
            print(f"Lower limit:{lower_limit_salary}")
            lower_limit_salary = int(lower_limit_salary.strip())
            print(lower_limit_salary)

            upper_limit_start_index = lower_limit_end_index+1
            upper_limit_end_index = salary.find("a")
            upper_limit_salary = salary[upper_limit_start_index: upper_limit_end_index]
            print(f"Upper limit {upper_limit_salary}")
            upper_limit_salary = int(upper_limit_salary.strip())
            print(upper_limit_salary)

            average_salary = (lower_limit_salary+upper_limit_salary)/2.0

            if salary.find("ayear")!=-1:
                average_salary = average_salary/12.0
                lower_limit_salary = lower_limit_salary/12.0
                upper_limit_salary = upper_limit_salary/12.0
            
            if salary.find("aweek")!=-1:
                average_salary = average_salary*4
                lower_limit_salary = lower_limit_salary*4
                upper_limit_salary = upper_limit_salary*4

            print(f"Lower limit:{lower_limit_salary}")
            print(f"Upper limit {upper_limit_salary}")
            
            return average_salary,lower_limit_salary, upper_limit_salary
    except:
        print("Error getting average salary")
        return salary,salary,salary

class visibilityOfNElementsLocatedBy(object):
    def __init__(self, locator, elementsCount_):
        self.locator = locator
        self.elementsCount = elementsCount_

    def __call__(self, driver):
        try:
            elements= driver.find_elements_by_xpath("//div[@class='ux-image handset-img v-large-top v-large-bottom']//img")
            if (len(elements) < elementsCount):
                return False
            else:
                return True
        except:
            return False


def get_jobs():

    global current_page
    global current_postings    
    global total_postings

    try:
        wait = WebDriverWait(driver, 500)
        has_next_page = False         
        
        print("Locating jobs....", end= ' ')
        jobs_visible = wait.until(EC.presence_of_element_located(JOB_CARD))
        print("Located jobs!")
    
    except:        
        print("Error locating job cards")

    try:         
        print("Locating search count....",end= ' ')
        search_count = wait.until(EC.presence_of_element_located(SEARCH_COUNT))
        print("Located search count")
        search_count_text = search_count.text
        
        page_count_start_index = 5
        page_count_end_index = search_count_text.find("of")
        
        current_page = int(search_count_text[page_count_start_index:page_count_end_index])
        #print(f"{page_count_start_index} {page_count_end_index} {current_page}")

        post_count_start_index = page_count_end_index + 3
        post_count_end_index = search_count_text.find(" jobs")
        #print(f"{post_count_start_index} {post_count_end_index}")
        total_postings_str = search_count_text[post_count_start_index:post_count_end_index].replace(",","")
        #print(f"{post_count_start_index} {post_count_end_index} {total_postings_str}")
        total_postings = int(total_postings_str)
        
        print(f"Showing {current_page} of {total_postings} postings")
    except:
        print("Error retrieving the page count")        
            
    try:           
        print("Locating navigation bar....",end= ' ')
        pagination_visible = wait.until(EC.element_to_be_clickable(PAGINATION))
        print("Located navigation bar!")
        all_children_by_tagname= pagination_visible.find_elements_by_tag_name("li")
        #print(f"Found {len(all_children_by_tagname)} navigation buttons")
            
    except:
        print("Error retrieving the navigation bar or navigation buttons")

    try:
        print("Locating next page button....", end= ' ')
        nextpagebutton_visible = all_children_by_tagname[len(all_children_by_tagname)-1]
        #nextpagebutton_visible = wait.until(EC.element_to_be_clickable(PAGINATION_PN))
        #nextpagebutton_visible = wait.until(EC.element_to_be_clickable(PAGINATION_PN))            
        #nextpage_button_visible = driver.find_element_by_link_text(current_page+1)
        #PAGINATION_PN = (By.CLASS_NAME, "pn")
        #all_input_tags = driver.find_elements_by_tag_name('input')
        #nextpagebutton_visible = driver.find_element_by_xpath("//span[contains(text(),current_page)]")
        ##driver.findElement(By.xpath("//*[text()=]"))
        print("Located next page button!")
        has_next_page = True
    except:
        nextpagebutton_visible = None
        has_next_page = False

    print("Retrieving all job cards....", end= ' ')
    job_cards = driver.find_elements_by_class_name("jobsearch-SerpJobCard")                
    print(f"Found {len(job_cards)} job cards")
        
    for i in range(0,len(job_cards)):
        job = {}
        element = job_cards[i]

        job_title = element.find_element(By.CLASS_NAME, 'title')
        job_company = element.find_element(By.CLASS_NAME, 'company')
        job_location = element.find_element(By.CLASS_NAME, 'location')
        job_link = job_title.find_element(By.TAG_NAME, "a")
        job_link_text = job_link.get_attribute('href')
        print(f"Job link {job_link_text}")

        try:
            job_salary = element.find_element(By.CLASS_NAME, 'salaryText')                
            job_salary_text = job_salary.text            
        except NoSuchElementException:
            job_salary_text = "Unknown"

        try:
            job_date = element.find_element(By.CLASS_NAME, 'date ')                
            job_date_text = job_date.text
        except NoSuchElementException:
            job_date_text = "Unknown"

        element_text = element.text
        
        job['description'] = element_text            
        job['title'] = job_title.text
        job['company'] = job_company.text
        job['location'] = job_location.text
        job['salary'] = job_salary_text
        job['average_salary'],job['lower_limit_salary'],job['upper_limit_salary'] = get_average_salary(job_salary_text)
        job['date'] = job_date_text
        job['link'] = job_link_text

        jobs.append(job)
        current_postings += len(jobs)
        
    return has_next_page, nextpagebutton_visible, current_page


def get_jobtitle_records(keywords,file_name,minimum_salary,location,radius):

    #file_name = "jobs_data_engineer.xlsx"
    #keywords = "data+engineer"
    #minimum_salary = "+$200000"
    #location = "Singapore"
    #radius = 50

    global current_page
    global current_postings    
    global total_postings

    try:    
        
        get_more_jobs = True

        current_page = 0
        current_postings = 0    
        total_postings = 999999

        while get_more_jobs and len(jobs) <total_postings:
            current_page+=1
            print(f"Getting page {current_page}")
            print(f"{len(jobs)} jobs scraped so far...")
            print()
            print()
            get_more_jobs, showmorejobs_visible, total_pages = get_jobs()                
            if get_more_jobs:
                countdown_stop = 5

                countdown(countdown_stop)        
                
                showmorejobs_visible.click()
                         
            else:
                print("No more jobs to scrape")                        

        print("Done!")

        print(f"Collected {len(jobs)} jobs")
        
        import pandas as pd

        df = pd.DataFrame(jobs)
        df.to_excel(file_name)

        print("Saved to file")

    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])

def generate_new_driver():

    ua = UserAgent()
    userAgent = ua.random

    options = Options()
    options.add_argument("--window-size=1920,1200")
    options.add_argument(f'user-agent={userAgent}')
        
    DRIVER_PATH = 'c:\chromedriver\chromedriver.exe'                
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)        

    return driver


if __name__ == "__main__":
    
    JOB_CARD = (By.CLASS_NAME, "jobsearch-SerpJobCard")
    PAGINATION = (By.CLASS_NAME, "pagination-list")
    PAGINATION_PN = (By.CLASS_NAME, "pn")
    SEARCH_COUNT = (By.ID, "searchCountPages")

    try:                  
        job_titles = pd.read_csv("jobtitles_usa.csv")     

        for index in job_titles.index:

            try:
            
                to_scrape = str(job_titles["to_scrape"][index]).lower()

                if to_scrape == 'y':                

                    driver = generate_new_driver()
                
                    file_name = job_titles["filename"][index]
                    keywords = job_titles["keywords"][index] # "machine+learning+engineer"
                    minimum_salary = "" if str(job_titles["minimum_salary"][index])=="nan" else str(job_titles["minimum_salary"][index])#"" if len(str(job_titles["minimum_salary"][index])) <0 else job_titles["minimum_salary"][index] #"+$200000"
                    location =  job_titles["location"][index] # "California"
                    radius = job_titles["radius"][index]  # 50
                    company = "" if str(job_titles["company"][index]) == "nan" else str(job_titles["company"][index])  # 50
                    #&rbc=

                    if len(company)>0:
                        URL = f"https://www.indeed.com/jobs?q={keywords}{minimum_salary}&l={location}&radius={radius}&rbc={company}"
                    else:
                        URL = f"https://www.indeed.com/jobs?q={keywords}{minimum_salary}&l={location}&radius={radius}"
                    
                    driver.get(URL)

                    jobs = []
                    
                    get_jobtitle_records(keywords,file_name,minimum_salary,location,radius)

                    sleep(20)

                    driver.quit()
            
            except:
                print(f"Error processing record {index}")
                for error in sys.exc_info():
                    print(error)
                continue
            
    except:
        print(f"Error running web scraping")
        for error in sys.exc_info():
            print(error)
