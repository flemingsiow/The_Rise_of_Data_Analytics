import sys
import pandas as pd

def merge_files(infile1_filename, infile2_filename, outfile_filename, how_to_merge, left_merge_column, right_merge_column):
    
    infile1_df = pd.read_excel(infile1_filename)
    infile2_df = pd.read_excel(infile2_filename)

    try:        
    
        print(f"Merging the two files: {infile1_filename} and {infile2_filename}")        
        
        result = pd.merge(infile1_df, infile2_df, how=how_to_merge, left_on=left_merge_column, right_on=right_merge_column)

        print("Successfully merged!")
        
        result.to_excel(outfile_filename)

    except:

        print("Error merging the files")
        for error in sys.exc_info():
            print(error)

def join_jobs_descriptions():
    infile1_filename = "combined_jobs_add_category_v001.xlsx"
    infile2_filename = "new_10_to_1575.xlsx"
    outfile_filename = "combined_jobs_add_category_add_description_v002.xlsx"
    how_to_merge = "left"
    left_merge_column = 'id'
    right_merge_column = 'id'

    merge_files(infile1_filename,infile2_filename,outfile_filename,how_to_merge,left_merge_column,right_merge_column)


if __name__ == "__main__":
    join_jobs_descriptions()
    
        



        
