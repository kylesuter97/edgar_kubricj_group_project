import ref_data as edgar_data
import edgar_downloader
import edgar_cleaner
import edgar_sentiment_wordcount as edgar_wordcount
import os

tickers = edgar_data.get_sp100()
def main(list_of_tickers=tickers, input_folder, output_folder, output_file):
    repo_wd = os.getcwd()
    for i in list_of_tickers:
        edgar_downloader.download_files_10k(i, input_folder) #Downloads all html files to folder

    edgar_cleaner.write_clean_html_text_files(input_folder, output_folder)#Cleans all files in folder
    os.chdir(repo_wd)
    sentiment_dict = edgar_data.get_sentiment_word_dict()
    os.chdir(repo_wd)
    edgar_wordcount.write_documents_sentiment_wordcount(output_folder, output_file, sentiment_dict)
    os.chdir(repo_wd)

main(tickers, 'C:\\NotOneDrive\\Edgar\\test_dir\\input_files', 'C:\\NotOneDrive\\Edgar\\test_dir\\output_files', 'C:\\NotOneDrive\\Edgar\\test_dir\\output3m.csv')
