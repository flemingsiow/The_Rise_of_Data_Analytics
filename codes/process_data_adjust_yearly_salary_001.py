import pandas as pd
import sys


def get_salary(salary,type_of_salary):
    
    average_salary = 0

    salary = salary.replace("$","")
    salary = salary.replace(",","")
    salary = salary.replace(" ","")

    #print(f"Salary is {salary}",end=" ")
    
    try:

        if salary.find("-") == -1:
            lower_limit_start_index = 0
            lower_limit_end_index = salary.find("a")
            lower_limit_salary = int(salary[lower_limit_start_index:lower_limit_end_index])
            upper_limit_salary = int(lower_limit_salary)
            average_salary = int(lower_limit_salary)
            #print(f"Salary without a range {salary}, average is {average_salary}")
        else:
            #2000 - 8000 a month
            lower_limit_start_index = 0
            lower_limit_end_index = salary.find("-")
            #print(lower_limit_start_index)
            #print(lower_limit_end_index)
            lower_limit_salary = salary[lower_limit_start_index:lower_limit_end_index]
            #print(f"Lower limit:{lower_limit_salary}")
            lower_limit_salary = int(lower_limit_salary.strip())
            #print(lower_limit_salary)

            upper_limit_start_index = lower_limit_end_index+1
            upper_limit_end_index = salary.find("a")
            upper_limit_salary = salary[upper_limit_start_index: upper_limit_end_index]
            #print(f"Upper limit {upper_limit_salary}")
            upper_limit_salary = int(upper_limit_salary.strip())
            #print(upper_limit_salary)

            average_salary = round((lower_limit_salary+upper_limit_salary)/2.0,0)

        if salary.find("ayear")!=-1:
            average_salary = round((average_salary/12.0),0)
            lower_limit_salary = round((lower_limit_salary/12.0),0)
            upper_limit_salary = round((upper_limit_salary/12.0),0)
        
        if salary.find("aweek")!=-1:
            average_salary = average_salary*4
            lower_limit_salary = lower_limit_salary*4
            upper_limit_salary = upper_limit_salary*4            
            
        if salary.find("aday")!=-1:
            average_salary = average_salary*4
            lower_limit_salary = lower_limit_salary*4
            upper_limit_salary = upper_limit_salary*4

        if salary.find("anhour")!=-1:
            average_salary = average_salary*8*20
            lower_limit_salary = lower_limit_salary*8*20
            upper_limit_salary = upper_limit_salary*8*20
        
            
        if type_of_salary == "Average Salary":
            print(f"Average Salary:{average_salary}")
            return average_salary
            
        elif type_of_salary == "Lower Limit Salary":
            print(f"Lower limit:{lower_limit_salary}")
            return lower_limit_salary
            
        elif type_of_salary == "Upper Limit Salary":
            print(f"Upper limit {upper_limit_salary}")
            return upper_limit_salary
        
        else:
            return "Unknown"

    except:
        print(f"Error getting {type_of_salary} with '{salary}'")
        return "Unknown"

    
def adjust_average_salary(col_value):
    
    col_new_value = get_salary(str(col_value), "Average Salary")
    return col_new_value

def adjust_lower_limit_salary(col_value):
    
    col_new_value = get_salary(str(col_value),"Lower Limit Salary")
    return col_new_value

def adjust_upper_limit_salary(col_value):
    
    col_new_value = get_salary(str(col_value),"Upper Limit Salary")
    return col_new_value


def main_job(infiles,column_name,functions_to_apply, columns_to_apply):        

    for f in infiles:

        df = pd.read_excel(f)
        filename_out = f"combined_jobs_add_category_add_description_adjust_salary_v002.xlsx"
    
        try:                
            for i in range(0,len(functions_to_apply)):
                function = functions_to_apply[i]
                column = columns_to_apply[i]
                df[column] = df[column_name].apply(function)
            
            df.to_excel(filename_out)

        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            print(sys.exc_info()[2])


def process_indeed():

    infiles = ["combined_jobs_add_category_add_description_v002.xlsx"]       
    functions_to_apply = [adjust_average_salary, adjust_lower_limit_salary, adjust_upper_limit_salary]
    columns_to_apply = ["average_salary", "lower_limit_salary", "upper_limit_salary"]
    column_name = "salary"
    main_job(infiles,column_name, functions_to_apply,columns_to_apply)


if __name__ == "__main__":

    process_indeed()
    