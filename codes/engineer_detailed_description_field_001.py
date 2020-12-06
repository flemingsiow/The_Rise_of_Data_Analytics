import pandas as pd
import sys

  
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
    
def main_job(oldfn,newfn,link_col,new_col,start_num,end_num):

    jobs_df = pd.read_excel(oldfn)    
    jobs = []

    try:
        for index in range(start_num,end_num):#jobs_df.index:
            job = {}
            job["id"] = jobs_df["id"][index]
            link = jobs_df[link_col][index]
            detailed_description = get_description(job["id"],link)
            job["detailed_description"] = detailed_description
            jobs.append(job)

            countdown(5)
    
        df = pd.DataFrame(jobs)
        df.to_excel(newfn)

    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])


def get_description(job_id,link):

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

    detailed_description = ""
    
    DRIVER_PATH = 'c:\chromedriver\chromedriver.exe'
    
    options = Options()
    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    wait = WebDriverWait(driver, 500)    
    driver.get(link)
    
    JOB_DESCRIPTION = (By.ID, "jobDescriptionText")

    try:            
        print(f"Trying to locate job description for {job_id}...", end= '\n')
        jd_visible = wait.until(EC.presence_of_element_located(JOB_DESCRIPTION))
        detailed_description = jd_visible.text
        driver.close()
    except:        
        print(f"Error locating the job description for this job {job_id}") 
        driver.close()
    
    return detailed_description


def do_main_job():

    loops = [1450,1475,1500,1525,1550,1575,1600,1625,1650,1675,1700]
    
    for num in loops:
        start_num=num
        end_num=num+50
        original_filename = "combined_jobs.xlsx"
        new_filename = f"new_{start_num}_to_{end_num}_{original_filename}"
        link_column = "link"
        new_column_name = "DescriptionDetailed"
            
        main_job(original_filename,new_filename,link_column, new_column_name,start_num,end_num)

        from time import sleep
        sleep(10)


if __name__ == "__main__":
    
    do_main_job()