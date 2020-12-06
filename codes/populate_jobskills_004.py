import pandas as pd
import sys

def analyse_skill_by_job(skill, job_id,job_field, records):

        variations = [
            " " + skill.lower() + " ", #' R '
            "," + skill.lower() + " ", #',R '
            "," + skill.lower() + " ", #',R '
            " " + skill.lower() + ",", #' R,'
            " " + skill.lower() + ", ", #" R, "
            " " + skill.lower() + "/", #" R/Python"
        ]
        for v in variations:
            if job_field.lower().find(v)!=-1:
                record = {}
                record['job_id'] = job_id
                record['skill'] = skill                
                records.append(record)
                break


def analyse_skill_by_job_old(skill, job_id,job_field, records):

    if len(skill)>1:
        if job_field.lower().find(skill.lower())!=-1:
            record = {}
            record['job_id'] = job_id
            record['skill'] = skill
            records.append(record)
    elif len(skill)==1:
        variations = [
            " " + skill.lower() + " ", #' R '
            "," + skill.lower() + " ", #',R '
            "," + skill.lower() + " ", #',R '
            " " + skill.lower() + ",", #' R,'
            " " + skill.lower() + ", ", #" R, "
            " " + skill.lower() + "/", #" R/Python"
        ]
        for v in variations:
            if job_field.lower().find(v)!=-1:
                record = {}
                record['job_id'] = job_id
                record['skill'] = skill
                records.append(record)
                break


def main_job(jobs_filename, skills_filename, jobskills_filename, skill_column, job_id_column, job_description_column,job_detailed_description_column):
    jobs = pd.read_excel(jobs_filename,index='id')
    skills = pd.read_excel(skills_filename)
    jobskills = []

    try:
        for index in skills.index:
            skill = str(skills[skill_column][index])
            populate_job_skills_dataset(skill,jobs,job_id_column, job_description_column,job_detailed_description_column,jobskills)

        jobskills_df = pd.DataFrame(jobskills)
        jobskills_df.to_excel(jobskills_filename)

    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])

def populate_job_skills_dataset(skill, jobs_df, id_column, description_column, detailed_description_column,skills_df):
    try:                          
        for index in jobs_df.index:
           job_id = str(jobs_df[id_column][index])    #str(index)
           description  = str(jobs_df[description_column][index])
           detailed_description = str(jobs_df[detailed_description_column][index])
           print(f"\n\nAnalysing for skill {skill}")
           print(f"job id: {job_id}")
           #print(f"description: {description} ")

           analyse_skill_by_job(skill,job_id,description,skills_df)
           analyse_skill_by_job(skill,job_id,detailed_description,skills_df)
                
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])


def get_individual():
    job_titles = pd.read_csv("jobtitles.csv")     
    skills_filename = "skills.xlsx"

    for index in job_titles.index:
        jobs_filename = job_titles["filename"][index]   
        jobskills_filename = jobs_filename.replace("jobs_","jobskills_")
        skill_column = "Skill"
        job_id_column = "id"
        job_description_column = "description"
        
        main_job(jobs_filename, skills_filename, jobskills_filename, skill_column, job_id_column, job_description_column)

def get_combined():

    from datetime import datetime
    dt = datetime.now()
    # Start a new file based on current timestamp
    fn = "{}{}{}{}{}{}".format(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second)
    
    skills_filename = "skills.xlsx"
    jobs_filename = "combined_jobs_add_category_add_description_adjust_salary_v002.xlsx"
    jobskills_filename = f"jobskills_{fn}.xlsx"
    skill_column = "Skill"
    job_id_column = "id"
    job_description_column = "description"
    job_detailed_description_column = "detailed_description"

        
    main_job(jobs_filename, skills_filename, jobskills_filename, skill_column, job_id_column, job_description_column,job_detailed_description_column)


if __name__ == "__main__":

    #get_individual()
    get_combined()