import pandas as pd
import sys
    
def remove_numbers(col_value):

    #col_new_value = str(col_value[0:-3])    
    col_new_value = (str(col_value))[0:-3]
    return col_new_value

def main_job(filename_in,filename_out,column_name,function_to_apply):        

    df = pd.read_excel(filename_in)
    
    try:
        #df['Name'] = df.Name.apply(upper)
        df[column_name] = df[column_name].apply(function_to_apply)
        df.to_excel(filename_out)
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])


if __name__ == "__main__":

    infiles = ["glassdoor/excel/Glassdoor Business Intelligence Analyst Jobs.csv.xlsx",
              "glassdoor/excel/Glassdoor Data Analyst Jobs.csv.xlsx",
              "glassdoor/excel/Glassdoor Data Engineer Jobs.csv.xlsx",
              "glassdoor/excel/Glassdoor Data Scientist Jobs.csv.xlsx",
              "glassdoor/excel/Glassdoor Machine Learning Engineer Jobs.csv.xlsx",
              "glassdoor/excel/Glassdoor Quantitative Analyst Jobs.csv.xlsx"]    

    for f in infiles:
        main_job(f,
             f"{f}_MODIFIED.xlsx",
             "Company Name",remove_numbers)
