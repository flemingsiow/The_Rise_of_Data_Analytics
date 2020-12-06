# https://revetice.readthedocs.io/en/latest/python/regular_expression.html

# for file in directory
# http://stackoverflow.com/questions/3964681/find-all-files-in-directory-with-extension-txt-with-python
## glob

def get_files_in_folder(folder,filename_pattern="*.*", save_to_file="files_in_directory.xlsx"):

    import pandas as pd    
    import glob
    import os

    files = []
    
    os.chdir(folder)
    for file in glob.glob(filename_pattern):
        files.append(file)

    df = pd.DataFrame(files)
    df.to_excel(save_to_file)


if __name__ == "__main__":
    
    folder = "D:\\Dropbox\\0_Programming\\2020\\2020-11_Nov\\2020-11-28 selenium python indeed\\glassdoor\\excel\\to_combine"
    filename_pattern = "*.xlsx"
    save_to_file = "glassdoor_data_merged.xlsx"
    get_files_in_folder(folder,filename_pattern,save_to_file)
