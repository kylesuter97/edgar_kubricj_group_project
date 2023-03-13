# Edgar-BPS


## Getting started

This repository has been developed as part of team Battersea Power Station's submission for the Edgar project.

This pipeline scrapes, cleans and analyzes S&P100 10-k submissions from the U.S. Securities and Exchange Commission's EDGAR Company filings.

The pipeline is split into 5 modules:

- Data Ingestion - "edgar_downloader"

- Data Cleaning - "edgar_cleaner"

- Reference Data Collecting - "ref_data"

- Sentiment Word Counting - "edgar_sentiment_wordcount"

- Sentiment Analysis

### Installation
Ensure correct packages are installed using the requirement.txt file as below
```
pip install requirements.txt -r
```
### Usage

The pipeline as a whole can be run by running the `run_pipeline.py` file, changing the input and output folder locations. By default the pipeline will be run on the entire S&P100, however a list of individual tickers can also be entered.

Running individual sections can also be done provided the required data is present, this is detailed further in the pipeline section below.

**IMPORTANT** : Throughout the pipeline when entering a path location, any uses of a `\` symbol must be replace with `\\` to ensure compatibility.
e.g. `'C:\Documents\testfolder\subfolder'` must be replaced with `'C:\\Documents\\testfolder\\subfolder'`



## Pipeline Modules:
### Data Ingestion: edgar_downloader
---

The edgar_downloader module can be used to download all 10-k submissions for a given S&P100 company, in the form of raw .htm files.

The code below can be used for example to download all 10-k submissions for Apple.

```
import edgar_downloader 
edgar_downloader.download_files_10k('AAPL', 'C:\\Documents\\testfolder\\subfolder')
```

Each file will be outputted with the naming convention:

`<ticker>_10-k_<filingdate>.htm `


### Data Cleaning: edgar_cleaner
---
The edgar_cleaner module can be used to clean any 10-k submissions in raw .htm format, removing any html tags, and outputting the clean text in .txt files.

The code below can be used for example to clean a folder of .htm files

```
import edgar_cleaner
edgar_cleaner.write_clean_html_text_files('C:\\Documents\\testfolder\\inputfolder', 'C:\\Documents\\testfolder\\outputfolder')
```

### Reference Data Collecting: ref_data
---
The ref_data module provides three functions that used in the pipeline:

- **Part A - get_sp100()**
The `get_sp100()` can be used to provide a list of the tickers of companies that are currently in the S&P100. The `run_pipeline.py` script will use this by default unless another list of ticker is provided instead.

The code below for example will print the described list
```
import ref_data
print(ref_data.get_sp100())
```

 - **Part B - get_yahoo_data()**


The `get_yahoo_data()` function can be used to generate a pandas  Data Frame of the yahoo financials of a given ticker between the start date and end date inputted. Columns consists of high, low, price, volume, different time spans of returns.

For example the below code can be used to generate a dataframe for AAPL between 2018-2020
```
import ref_data
print(ref_data.get_yahoo_data('2018-01-10', '2020-01-01', 'AAPL'))
```


- **Part C - get_sentiment_word_dict()**

The `get_sentiment_word_dict()` function can be used to provide a dictionary for sentiment values: Postive, Negative, Uncertainty, Litigious, Constraining, Superfluous, Interesting, Modal.

For example, the code below will print all the words associated with the "Negative" sentiment
```
import ref_data as edgar_data
sentiment_dict = edgar_data.get_sentiment_word_dict()['Negative']
print(sentiment_dict)
```


### Sentiment Word Counting: edgar_sentiment_wordcount
---
The edgar_sentiment_wordcount module is used read in a folder of 10-k submissions that have been cleaned by the edgar_cleaner module, count the number of words in each document belonging to a particular sentiment and outputs the results to the output .csv file.

The code below for example will return a .csv file from the 10-k submission .txt files in the folder
```
import edgar_sentiment_wordcount as edgar_sentiment
edgar_sentiment.write_document_sentiments('C:\\Documents\\testfolder\\inputfolder', 'C:\\Documents\\testfolder\\output.csv')
```


#### Sentiment Data Analysis: sentiment_analysis
---

The sentiment_analysis module takes in tables created through sentiment extraction and reference data acquisition and merges them into one table before performing regression analyses and producing relevant graphs.

Currently can only be run as part of whole pipeline as in `run_pipeline.py` - will be updated to also run with pre-made sentiment + reference .csv files.