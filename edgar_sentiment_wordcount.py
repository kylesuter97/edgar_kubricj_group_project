import os
import pandas as pd
import re
from nltk import word_tokenize
from nltk.corpus import stopwords
import ref_data as edgar_data

def write_documents_sentiments(input_folder, output_file): #Main Function
    def name_cleaner(filename): #Function for getting Symbol, ReportType, FilingDate
        filenamelist = filename.split('_') #Split file name by _
        symbol = filenamelist[0]
        reporttype = filenamelist[1]
        filingdatetxt = filenamelist[2]
        filingdate = filingdatetxt.split('.')[0] #remove .txt from date
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
            if i in sentiment_dict["Positive"]:
                positive += 1
            elif i in sentiment_dict["Negative"]:
                negative += 1
            elif i in sentiment_dict["Litigious"]:
                litigious += 1
            elif i in sentiment_dict["Constraining"]:
                constraining += 1
            elif i in sentiment_dict["Superfluous"]:
                superfluous += 1
            elif i in sentiment_dict["Interesting"]:
                interesting += 1
            elif i in sentiment_dict["Uncertainty"]:
                uncertainty += 1
            elif i in sentiment_dict["Modal"]:
                modal += 1
        #returns all sentiment counts 
        return positive, negative, uncertainty, litigious, constraining, superfluous, interesting, modal

    def read_text_file(file_path): # Function for reading in each word in html, removing punctuation, captilizing and removing stopwords
        with open(file_path, 'r', encoding='utf-8') as f:
            output = f.read()
        output = output.upper() #Upper text to match LM dict
        output = re.sub(r'[^A-Za-z0-9]', ' ', output) #remove punctuation
        unclean_token_list = word_tokenize(output) #Put all words in list
        token_list = [] #Empty list to append to
        for word in unclean_token_list:
            if word not in stopword_list: #Appends word if not in stop_words
                token_list.append(word)
            else:
                pass
        return token_list

    #Create empty pandas df with required headings
    columnheaders=['Symbol', 'ReportType', 'FilingDate', 'Negative', 'Positive', 'Uncertainty', 
                                'Litigious', 'Constraining', 'Superfluous', 'Interesting', 'Modal']
    
    #Stopword list of words to ignore
    stopword_list = stopwords.words('english')

    #Create empty list of dicts for later dataframe
    lod = []

    sentiment_dict = edgar_data.get_sentiment_word_dict()
    #Change directory to input folder
    os.chdir(input_folder)
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

            #Print out that 1 report appended
            print(f"Extracted data from {file}")
    #Create dataframe of all html files sentiment counts
    df = pd.DataFrame(lod, columns=columnheaders)
    sentiment_df = df
    #Preview dataframe
    print(df)

    #Output to required folder
    os.chdir(input_folder)
    df.to_csv(output_file)
    return sentiment_df
