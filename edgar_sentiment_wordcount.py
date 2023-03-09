import os
import pandas as pd

def write_documents_sentiment_wordcount(input_folder, output_file):
    #Create empty pandas df with required headings
    df = pd.DataFrame(columns=['Sybmol', 'ReportType', 'FilingDate', 'Negative', 'Positive', 'Uncertainty', 
                               'Litigous', 'Constraining', 'Superflous', 'Interesting', 'Modal'])
    display(df)


    #########################################
    #Change directory to input folder
    os.chdir(input_folder)

    #iterate through every file in folder
    for file in os.listdir():
        #Check if file is a text file
        if file.endswith(".txt"):
            file_path = f"{input_folder}\{file}"
            with open(file_path, 'r') as f:
                #need to figure 
        else:
            pass
    #########################################




    pass
