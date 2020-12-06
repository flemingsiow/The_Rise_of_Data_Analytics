import sys
import pandas as pd


def combine_files(files_to_combine_csv, output_filename):
    from datetime import datetime
    dt = datetime.now()
    # Start a new file based on current timestamp
    fn = "{}{}{}{}{}{}".format(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second)

    files_to_combine = pd.read_csv(files_to_combine_csv)    
    combined_df = []
    
    for index in files_to_combine.index:

        to_combine = str(files_to_combine["to_combine"][index]).lower()

        if to_combine=='y':
            
            filename = files_to_combine["filename"][index]            
            
            df = pd.read_excel(filename)
            print(f"Appending {filename} with {len(df)} records")        
            combined_df.append(df)    

    result = pd.concat(combined_df)

    result.to_excel(output_filename)



def combine_jobfiles():
    from datetime import datetime
    dt = datetime.now()
    # Start a new file based on current timestamp
    fn = "{}{}{}{}{}{}".format(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second)

    job_titles = pd.read_csv("jobtitles.csv")
    output_filename = f"combined_jobs_{fn}.xlsx"
    combined_df = []
    
    for index in job_titles.index:

        to_combine = str(job_titles["to_combine"][index]).lower()

        if to_combine=='y':
            jobs_filename = job_titles["filename"][index]
            
            
            df = pd.read_excel(jobs_filename)
            print(f"Appending {jobs_filename} with {len(df)} records")        
            combined_df.append(df)    

    result = pd.concat(combined_df)

    result.to_excel(output_filename)


def combine_glassdoor():

    files_to_combine_csv = "files_to_combine_glassdoor.csv"
    output_file = "glassdoor_combined.xlsx"
    combine_files(files_to_combine_csv,output_file)

def files_to_combine_detailed_descriptions():
    files_to_combine_csv = "files_to_combine_detailed_descriptions.csv"
    output_file = "new_10_to_1575.xlsx"
    combine_files(files_to_combine_csv,output_file)

if __name__ == "__main__":

    #combine_glassdoor()
    files_to_combine_detailed_descriptions()
    

        
