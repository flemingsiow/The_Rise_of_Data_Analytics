import pandas as pd
import sys
    

def main_job(original_filename, num_columns, new_filename):        

    df = pd.read_csv(original_filename,usecols=range(num_columns), lineterminator='\n')
    
    try:
        df.to_excel(new_filename)
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])


def convert_glassdoor():

    infiles = ["glassdoor/Glassdoor Business Intelligence Analyst Jobs.csv","glassdoor/Glassdoor Data Analyst Jobs.csv",
              "glassdoor/Glassdoor Data Engineer Jobs.csv","glassdoor/Glassdoor Data Scientist Jobs.csv","glassdoor/Glassdoor Machine Learning Engineer Jobs.csv",
              "glassdoor/Glassdoor Quantitative Analyst Jobs.csv"]    
    num_cols = 14

    for f in infiles:
        main_job(f,num_cols,f"{f}.xlsx")

if __name__ == "__main__":

    convert_glassdoor()
