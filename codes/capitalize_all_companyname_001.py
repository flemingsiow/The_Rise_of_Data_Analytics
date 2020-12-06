import pandas as pd
import sys
    
def capitalize(col_value):
    
    col_new_value = str(col_value).upper()
    return col_new_value

def remove_full_stops(col_value):
    col_new_value = str(col_value).replace(".","")    
    return col_new_value

def strip_left_and_right(col_value):
    col_new_value = str(col_value).rstrip()
    col_new_value = str(col_value).lstrip()
    return col_new_value

def main_job(filename_in,filename_out,column_name,functions_to_apply):        

    df = pd.read_excel(filename_in)
    
    try:        
        for function in functions_to_apply:
            df[column_name] = df[column_name].apply(function)        
        
        df.to_excel(filename_out)
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])


def process_indeed():

    infiles = ["combined_jobs_add_category_add_description_v001.xlsx"]    

    functions = [capitalize, remove_full_stops, strip_left_and_right]

    for f in infiles:
        main_job(f,
             f"{f}_MODIFIED.xlsx",
             "company",functions)


def process_glassdoor():

    infiles = ["glassdoor_combined.xlsx"]    

    functions = [capitalize, remove_full_stops, strip_left_and_right]

    for f in infiles:
        main_job(f,
             f"{f}_MODIFIED.xlsx",
             "Company Name",functions)


if __name__ == "__main__":

    #process_glassdoor()
    process_indeed()
    