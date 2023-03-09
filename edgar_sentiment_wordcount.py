import os
import pandas as pd
import re
import json
from nltk import word_tokenize
from nltk.corpus import stopwords

def write_documents_sentiment_wordcount(input_folder, output_file): #Main Function
    def name_cleaner(filename): #Function for getting Symbol, ReportType, FilingDate
        filenamelist = filename.split('_')
        symbol = filenamelist[0]
        reporttype = filenamelist[1]
        filingdatetxt = filenamelist[2]
        filingdate = filingdatetxt.split('.')[0]
        return symbol, reporttype, filingdate
    
    def dict_creator(token_list): #Function for getting sentiment word counts per html 
        #initialise each sentiment counter to zero for every html
        positive = 0
        negative = 0
        uncertainty = 0
        litigious = 0
        constraining = 0
        superfluous = 0
        interesting = 0
        modal = 0

        #Counts every time a sentiment value appears
        for i in token_list:
            if i in positive_list:
                positive += 1
            elif i in negative_list:
                negative += 1
            elif i in litigious_list:
                litigious += 1
            elif i in constraining_list:
                constraining += 1
            elif i in superfluous_list:
                superfluous += 1
            elif i in interesting_list:
                interesting += 1
            elif i in uncertainty_list:
                uncertainty += 1
            elif i in modal_list:
                modal += 1
        #returns all sentiment counts 
        return positive, negative, uncertainty, litigious, constraining, superfluous, interesting, modal

    def read_text_file(file_path): # Function for reading in each word in html, removing punctuation, captilizing and removing stopwords
        with open(file_path, 'r', encoding='utf-8') as f:
            output = f.read()
        output = output.upper() #Upper text to match LM dict
        output = re.sub(r'[^A-Za-z0-9]', ' ', output) #remove punctuation
        unclean_token_list = word_tokenize(output)
        token_list = []
        for word in unclean_token_list:
            if word not in stopword_list:
                token_list.append(word)
            else:
                pass
        return token_list

    #Create empty pandas df with required headings
    columnheaders=['Symbol', 'ReportType', 'FilingDate', 'Negative', 'Positive', 'Uncertainty', 
                                'Litigious', 'Constraining', 'Superfluous', 'Interesting', 'Modal']
    
    #Stopword list of words to ignore
    stopword_list = stopwords.words('english')

    ###################################################################################################
    #Main part of Code
    ###############################################################################################


    #Change directory to input folder
    os.chdir(input_folder)
    temp_file_path = "C:\\NotOneDrive\\Edgar\\edgar-bps\\test_data.txt" # Nixon's LM dictionary..
    with open(temp_file_path, 'r', encoding='utf-8') as f:
        data = f.read()
        data = data.replace("'", '"')
    lm_dict = json.loads(data)

    #Create lists for individual sentiments
    positive_list = lm_dict['Positive']
    negative_list = lm_dict['Negative']
    uncertainty_list = lm_dict['Uncertainty']
    litigious_list = lm_dict['Litigious']
    constraining_list = lm_dict['Constraining']
    # superfluous_list = lm_dict['Superfluous']
    superfluous_list = ['redundant', 'unneeded']
    # interesting_list = lm_dict['Interesting']
    interesting_list = ['absorbing', 'engrossing']
    # modal_list = lm_dict['Modal]
    modal_list = []
    
    
    
    #Create empty list of dicts for later dataframe
    lod = []# LOD to make datafram

    #iterate through every file in folder
    for file in os.listdir():
        #Check if file is a text file
        if file.endswith(".txt"):
            file_path = f"{input_folder}\{file}"
            #Create first 3 values from file name
            symbol, reporttype, filingdate = name_cleaner(file)

            #Create list of every word in html, cleaned and captialized
            token_list = read_text_file(file_path)

            #Return number of times each sentiment appears in html
            positive, negative, uncertainty, litigious, constraining, superfluous, interesting, modal = dict_creator(token_list)

            #Create temp dictionary for the primary lod
            tempdict = {"Symbol": symbol, "ReportType": reporttype, "FilingDate" : filingdate,
                        "Positive": positive, "Negative": negative, "Uncertainty": uncertainty, 
                        "Litigious": litigious, "Constraining": constraining, 
                        "Superfluous": superfluous, "Interesting": interesting,
                        "Modal": modal}
            #Append dictionary to LOD for dataframe
            lod.append(tempdict)
    #Create dataframe of all html files sentiment counts
    df = pd.DataFrame(lod, columns=columnheaders)

    #Preview dataframe
    print(df)

    #Output to required folder
    df.to_csv(output_file)


write_documents_sentiment_wordcount('C:\\NotOneDrive\\Edgar\\clean_html\\', 'C:\\NotOneDrive\\Edgar\\clean_html\outputfile.csv')