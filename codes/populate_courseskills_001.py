import pandas as pd
import sys

def analyse_skill_by_course(skill, course_id,course_field, records):

        print(f"Analysing for {course_field}")

        variations = [
            " " + skill.lower() + " ", #' R '
            "," + skill.lower() + " ", #',R '
            "," + skill.lower() + " ", #',R '
            " " + skill.lower() + ",", #' R,'
            " " + skill.lower() + ", ", #" R, "
            " " + skill.lower() + "/", #" R/Python"
        ]
        for v in variations:
            if course_field.lower().find(v)!=-1:
                record = {}
                record['courseid'] = course_id
                record['skill'] = skill                
                records.append(record)
                break


def analyse_skill_by_course_old(skill, course_id,course_field, records):

    if len(skill)>1:
        if course_field.lower().find(skill.lower())!=-1:
            record = {}
            record['courseid'] = course_id
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
            if course_field.lower().find(v)!=-1:
                record = {}
                record['courseid'] = course_id
                record['skill'] = skill
                records.append(record)
                break

#course_description_column,course_detailed_description_column
def main_course(courses_filename, skills_filename, courseskills_filename, skill_column, course_id_column, desc_cols):
    courses = pd.read_excel(courses_filename)
    skills = pd.read_excel(skills_filename)
    courseskills = []

    try:
        for index in skills.index:
            skill = str(skills[skill_column][index])
            populate_course_skills_dataset(skill,courses,course_id_column, desc_cols,courseskills)

        courseskills_df = pd.DataFrame(courseskills)
        courseskills_df.to_excel(courseskills_filename)

    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])

# description_column, detailed_description_column, detailed_description_column_2
def populate_course_skills_dataset(skill, courses_df, id_column, descriptions,skills_df):
    try:                          
        for index in courses_df.index:
           course_id = str(courses_df[id_column][index])    #str(index)
           #description  = str(courses_df[description_column][index])
           #detailed_description = str(courses_df[detailed_description_column][index])
           print(f"\n\nAnalysing for skill {skill}")
           print(f"course id: {course_id}")
           #print(f"description: {description} ")

           for description in descriptions:
               description_text = courses_df[description][index]
               analyse_skill_by_course(skill,course_id,description_text,skills_df)
            #analyse_skill_by_course(skill,course_id,detailed_description,skills_df)
                
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])


def get_individual():
    course_titles = pd.read_csv("coursetitles.csv")     
    skills_filename = "skills.xlsx"

    for index in course_titles.index:
        courses_filename = course_titles["filename"][index]   
        courseskills_filename = courses_filename.replace("courses_","courseskills_")
        skill_column = "Skill"
        course_id_column = "id"
        course_description_column = "description"
        
        main_course(courses_filename, skills_filename, courseskills_filename, skill_column, course_id_column, course_description_column)

def get_combined():

    from datetime import datetime
    dt = datetime.now()
    # Start a new file based on current timestamp
    fn = "{}{}{}{}{}{}".format(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second)
    
    skills_filename = "skills.xlsx"
    courses_filename = "skillsfuture_courses_002.xlsx"
    courseskills_filename = f"courseskills_{fn}.xlsx"
    skill_column = "Skill"
    course_id_column = "courseid"
    course_description_column = "full_course_title"
    course_detailed_description_column = "course_objectives"
    course_detailed_description_column_2 = "course_content"
    #full_course_title	course_objectives	course_content

    desc_columns = [course_description_column, course_detailed_description_column, course_detailed_description_column_2]
        
    main_course(courses_filename, skills_filename, courseskills_filename, skill_column, course_id_column, desc_columns)


if __name__ == "__main__":

    #get_individual()
    get_combined()