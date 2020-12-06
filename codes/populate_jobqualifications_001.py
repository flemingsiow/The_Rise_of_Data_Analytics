import pandas as pd
import sys

def analyse_qualification_by_job(qualification, job_id,job_field, records):

        qualification = qualification.lower()

        qualifications = qualification.split("||")

        for q in qualifications:

            variations = [
                " " + q.lower() + " ", #' R '
                "," + q.lower() + " ", #',R '
                "," + q.lower() + " ", #',R '
                " " + q.lower() + ",", #' R,'
                " " + q.lower() + ", ", #" R, "
                " " + q.lower() + "/", #" R/Python"
            ]
            for v in variations:
                print(f"Trying to find {v}")
                if job_field.lower().find(v)!=-1:
                    record = {}
                    record['job_id'] = job_id
                    record['qualification'] = qualifications[0]
                    records.append(record)
                    break

def main_job(jobs_filename, qualifications_filename, jobqualifications_filename, qualification_column, job_id_column, job_description_column,job_detailed_description_column):
    jobs = pd.read_excel(jobs_filename,index='id')
    qualifications = pd.read_excel(qualifications_filename)
    jobqualifications = []

    try:
        for index in qualifications.index:
            qualification = str(qualifications[qualification_column][index])
            populate_job_qualifications_dataset(qualification,jobs,job_id_column, job_description_column,job_detailed_description_column,jobqualifications)

        jobqualifications_df = pd.DataFrame(jobqualifications)
        jobqualifications_df.to_excel(jobqualifications_filename)

    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])

def populate_job_qualifications_dataset(qualification, jobs_df, id_column, description_column, detailed_description_column,qualifications_df):
    try:                          
        for index in jobs_df.index:
           job_id = str(jobs_df[id_column][index])    #str(index)
           description  = str(jobs_df[description_column][index])
           detailed_description = str(jobs_df[detailed_description_column][index])
           print(f"\n\nAnalysing for qualification {qualification}")
           print(f"job id: {job_id}")
           #print(f"description: {description} ")

           analyse_qualification_by_job(qualification,job_id,description,qualifications_df)
           analyse_qualification_by_job(qualification,job_id,detailed_description,qualifications_df)
                
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])


def get_individual():
    job_titles = pd.read_csv("jobtitles.csv")     
    qualifications_filename = "qualifications.xlsx"

    for index in job_titles.index:
        jobs_filename = job_titles["filename"][index]   
        jobqualifications_filename = jobs_filename.replace("jobs_","jobqualifications_")
        qualification_column = "qualification"
        job_id_column = "id"
        job_description_column = "description"
        
        main_job(jobs_filename, qualifications_filename, jobqualifications_filename, qualification_column, job_id_column, job_description_column)

def get_combined():

    from datetime import datetime
    dt = datetime.now()
    # Start a new file based on current timestamp
    fn = "{}{}{}{}{}{}".format(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second)
    
    qualifications_filename = "qualifications.xlsx"
    jobs_filename = "combined_jobs_add_category_add_description_adjust_salary_v002.xlsx"
    jobqualifications_filename = f"jobqualifications_{fn}.xlsx"
    qualification_column = "Qualification"
    job_id_column = "id"
    job_description_column = "description"
    job_detailed_description_column = "detailed_description"

        
    main_job(jobs_filename, qualifications_filename, jobqualifications_filename, qualification_column, job_id_column, job_description_column,job_detailed_description_column)


if __name__ == "__main__":

    #get_individual()
    get_combined()