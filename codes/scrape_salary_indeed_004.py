from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys 
from time import sleep
import sys

import pandas as pd


def get_company(companyname):

    global driver
    global wait

    URL = f"https://sg.indeed.com/salaries?from=gnav-recordsearch--jasx"
    driver.get(URL)

    wait = WebDriverWait(driver, 10)

    try:            
        print(f"Locating textfield and button....for {companyname}", end= ' ')
        textfield_visible = wait.until(EC.presence_of_element_located(SEARCH_COMPANY_TEXTFIELD))
        button_visible = wait.until(EC.element_to_be_clickable(SEARCH_COMPANY_BUTTON))        
        print(f"Located the textfield and button for {companyname}")
    except:        
        print("Error locating the textfield and button")
        return False
    
    try:            
        print(f"Sending data for {companyname}", end= ' ')
        textfield_visible.send_keys(companyname)
        
        autocomplete_visible = wait.until(EC.presence_of_element_located(SEARCH_COMPANY_AUTOCOMPLETE))
        autocomplete_visible.click()

        return True
        
    except:        
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print(f"Part 1 Error: Error sending data to fetch company records of {companyname}")

        return False    
    

def get_company_records(companyname):
    
    global driver
    global wait

    global get_more_records

    global current_page
    global current_records
    global total_records

    try:    

        while get_more_records and len(records) < total_records:
            current_page+=1

            print(f"Getting page {current_page}")
            print(f"{len(records)} records scraped so far...")
            print()
            print()

            get_more_records, showmorerecords_button, total_pages = get_records(companyname)                
            if get_more_records:
                #print("Scraping the next page of records...")
                showmorerecords_button.click()            
            else:
                print("No more records to scrape")                        


        ## https://selenium-python.readthedocs.io/waits.html
        print("Done!")

        print(f"Collected {len(records)} records")
        
        import pandas as pd

        global file_name

        df = pd.DataFrame(records)
        df.to_excel(file_name)

        print("Saved to file")
        print()
        print()
    
    except:
        print("Error getting company records")


def store_records(companyname,record_cards):
    
    global records
    global current_records 

    try:

        for i in range(0,len(record_cards)):
            
            print(f"Processing record {i} of {len(record_cards)}")
            record = {}
            element = record_cards[i]

            try:
                record_title = element.find_element(By.CLASS_NAME, 'cmp-SalarySummaryTitle-text')                    
                record_title_text = record_title.text
            
            except NoSuchElementException:
                record_title_text = "Unknown"
                
            try:
                record_salary = element.find_element(By.CLASS_NAME, 'cmp-SalarySummaryAverage-salary')                    
                record_salary_text = record_salary.text
            
            except NoSuchElementException:
                record_salary_text = "Unknown"
            
            record['title'] = record_title_text
            record['salary'] = record_salary_text.translate({ord(i): None for i in '$,'})
            record['company'] = companyname

            records.append(record)
            current_records += len(records)        
        
    except:

            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            print(f"Error inside the storerecords function")
            sys.exit(1)



def get_records(companyname):

    global driver
    global wait

    global current_page
    global current_records    
    global total_records
            
    has_next_page = False   

    try:            
        print("Locating records....", end= ' ')
        records_visible = wait.until(EC.presence_of_element_located(RECORDS_ELEMENT))
        print("Located records!")        
    except:        
        print("Error locating records")

    try:
        get_more_records = False
        showmorerecords_button = None
        total_pages=1
        print("Retrieving all record rows....", end= ' ')
        record_elements = driver.find_elements_by_class_name("cmp-SalarySummary-columns")
        print(f"Found {len(record_elements)} record rows")

        store_records(companyname, record_elements)

        return get_more_records, showmorerecords_button, total_pages

    except:
        print("Error getting records from the company")
            
    
if __name__ == "__main__":

    DRIVER_PATH = 'c:\chromedriver\chromedriver.exe'
    
    options = Options()
    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    wait = WebDriverWait(driver, 10)

    
    SEARCH_COMPANY_TEXTFIELD = (By.ID, "cmp-salary-search-input")
    SEARCH_COMPANY_BUTTON = (By.ID, "cmp-salary-search-submit")
    SEARCH_COMPANY_AUTOCOMPLETE = (By.CLASS_NAME, "cmp-salary-search-result-comp")
    RECORDS_ELEMENT = (By.CLASS_NAME, "cmp-PaginatedCategories")
    
    #records = []
    #get_more_records = True
    #current_page = 0
    #current_records = 0    
    #total_records = 999999

    try:                  
        companies = pd.read_excel("jobs_data_engineer.xlsx") 
        unique_companies = companies.company.unique()

        for companyname in unique_companies:
            records = []
            get_more_records = True
            current_page = 0
            current_records = 0    
            total_records = 999999
            company_info_available = get_company(companyname)
            if company_info_available:
                file_name = f"records_salaries_{companyname}.xlsx"
                print(f"Getting company records of {companyname}")
                get_company_records(companyname)

    finally:
        driver.quit()
