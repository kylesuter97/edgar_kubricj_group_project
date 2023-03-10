# Edgar-BPS


## Getting started

This is team  Battersea Power Station's submission for the Edgar project.

This pipeline scrapes, cleans and analyzes S&P100 10-k submissions from the U.S. Securities and Exchange Commission's EDGAR Company filings.

The pipeline is split into 4 sections:

- Data Ingestion

- Data Cleaning

- Sentiment Word Counting

- Sentiment Analysis

## Installation
Ensure correct packages are installed 
```
pip install requirements -r
```
## Usage

The pipeline as a whole can be run by running the 'Run_pipeline.py' file, changing the input and output folder locations. By default the pipeline will be run on the entire S&P100, however a list of individual tickers can also be entered.

Running individual sections can also be done assuming the required data is present, this is detailed further in the pipeline section below.


## Pipeline
### Part 1 - Data Ingestions
(Using Selenium)
Module called edgar_downloader, consists of 2 functions:
1. write_page(url, file_path)
    This will take in a URL and write the html to path specified
2. download_files_10k(ticker, dest_folder)
    Downloads all html 10-k files to dest_folder. 
    Convention: "<ticker>_10-k_<filing_date>.html"
Follow with Unit tests

### Part 2 - Data Preparation / Cleaning
(Using BeautifulSoup)
Module called edgar_cleaner. The module should contain the following functions: 
1.  clean_html_text(html_text)
Takes in a html text string and removes tags and special characters. Returns result as a string.
2.  write_clean_html_text_files(input_folder, dest_folder)
Takes all the html 10-k files in the input folder, cleans them using the clean_html_text function 
and writes them into the destination folder as text files. Files downloaded should follow the 
naming convention: <ticker>_10-k_<filing_date>.txt.

Follow with unit tests
### Part 3a - Reference Data: S&P100 Data
(Using API requests)
Module called ref_data. The module should contain the following functions: 
- get_sp100()
Returns a list of all tickers in the S&P100. Note that this can be a snapshot of the current 
constituents of the S&P100 and does not need to be updated live.

### Part 3B - Reference Data: Yahoo Finance 
(Using yahoofinancials)
Update the ref_data module. The module should contain the following added function: 
- get_yahoo_data(start_date, end_date, tickers)
Downloads yahoo finance data and consolidates all data into one table. In addition, returns 
should be calculated for 1, 2, 3, 5 and 10 business day time horizons. For example, the 1-day 
return is the return made if the stock was bought today and sold the next day. Returns a 
dataframe.

### Part 3C - Reference Data: Loughran-McDonald Sentiment Words
(Using NLP pre-processing and )
Update the ref_data module. The module should contain the following added function: 
- get_sentiment_word_dict()
Returns a dictionary containing the LM sentiment words. The keys for the dictionary are the 
sentiments, and the values will be a list of words associated with that particular sentiment. For 
example, get_sentiment_word_dict()[‘Negative’] will return a list of words associated with 
negative sentiment.

### Part 4 - Sentiment Word Counts
(Using feature extraction?)
module called edgar_sentiment_wordcount. The module should contain the following 
function: 
- write_document_sentiments(input_folder, output_file)
Takes all the clean text 10-k files in the input folder, counts the number of words in the 
document belonging to a particular sentiment and outputs the results to the output file

#### Part 5 - Sentiment Analysis
(Using general NLP modelling?)
### Post-Pipeline


