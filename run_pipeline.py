import ref_data as edgar_data
import edgar_downloader
import edgar_cleaner
import edgar_sentiment_wordcount as edgar_sentiment
import ref_data as edgar_data
import sentiment_analysis
import os

tickers = edgar_data.get_sp100()
def main(list_of_tickers, input_folder, output_folder, output_file, start_date, end_date):
    repo_wd = os.getcwd() #Recordws local repository
    # for i in list_of_tickers:
    #     edgar_downloader.download_files_10k(i, input_folder) #Downloads all html files to folder

    # edgar_cleaner.write_clean_html_text_files(input_folder, output_folder)#Cleans all files in folder
    os.chdir(repo_wd) #Returns to local directory
    sentiment_df = edgar_sentiment.write_documents_sentiments(output_folder, output_file)
    financials_df = edgar_data.get_yahoo_data(start_date,end_date, list_of_tickers)
    os.chdir(repo_wd)
    sentiment_analysis.analysis(sentiment_df, financials_df)

tickers = ['META']
main(tickers, 'C:\\NotOneDrive\\Edgar\\test_dir\\input_files', 'C:\\NotOneDrive\\Edgar\\test_dir\\output_files', 
     'C:\\NotOneDrive\\Edgar\\test_dir\\output3m.csv', '2018-01-01', '2023-01-01')
