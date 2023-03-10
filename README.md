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
Ensure correct packages are installed using the requirement.txt file as below
```
pip install requirements.txt -r
```
## Usage

The pipeline as a whole can be run by running the 'run_pipeline.py' file, changing the input and output folder locations. By default the pipeline will be run on the entire S&P100, however a list of individual tickers can also be entered.

Running individual sections can also be done provided the required data is present, this is detailed further in the pipeline section below.

**IMPORTANT** : Throughout the pipeline when entering a path location, any uses of a `\` symbol must be replace with `\\` to ensure compatibility.
e.g. `C:\Documents\testfolder\subfolder` must be replaced with `C:\\Documents\\testfolder\\subfolder`



## Pipeline Modules:
### Module 1: edgar_downloader
---

The edgar_downloader module can be used to download all 10-k submissions for a given S&P100 company, in the form of raw .htm files.

The code below can be used for example to download all 10-k submissions for Apple.

```
import edgar_downloader 
edgar_downloader.download_files_10k('AAPL', 'C:\\Documents\\testfolder\\subfolder')
```

Each file will be outputted with the naming convention:

`<ticker>_10-k_<filingdate>.htm `


### Module 2: edgar_cleaner
---
The edgar_cleaner module can be used to any 10-k submissions 


### Module 3: ref_data
---
(Using API requests)
Module called ref_data. The module should contain the following functions: 
- get_sp100()
Returns a list of all tickers in the S&P100. Note that this can be a snapshot of the current 
constituents of the S&P100 and does not need to be updated live.


### Part 3B - Reference Data: Yahoo Finance 
---
(Using yahoofinancials)
Update the ref_data module. The module should contain the following added function: 
- get_yahoo_data(start_date, end_date, tickers)
Downloads yahoo finance data and consolidates all data into one table. In addition, returns 
should be calculated for 1, 2, 3, 5 and 10 business day time horizons. For example, the 1-day 
return is the return made if the stock was bought today and sold the next day. Returns a 
dataframe.

### Part 3C - Reference Data: Loughran-McDonald Sentiment Words
---
(Using NLP pre-processing and )
Update the ref_data module. The module should contain the following added function: 
- get_sentiment_word_dict()
Returns a dictionary containing the LM sentiment words. The keys for the dictionary are the 
sentiments, and the values will be a list of words associated with that particular sentiment. For 
example, get_sentiment_word_dict()[‘Negative’] will return a list of words associated with 
negative sentiment.



### Part 4 - Sentiment Word Counts
---
(Using feature extraction?)
module called edgar_sentiment_wordcount. The module should contain the following 
function: 
- write_document_sentiments(input_folder, output_file)
Takes all the clean text 10-k files in the input folder, counts the number of words in the 
document belonging to a particular sentiment and outputs the results to the output file


#### Part 5 - Sentiment Analysis
---
(Using general NLP modelling?)
