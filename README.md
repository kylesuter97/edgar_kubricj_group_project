# Edgar-BPS



## Getting started

This is an initial place for us to get started on the Edgar project.

## Pre-Pipeline


## Pipeline
## Part 1 - Data Ingestions
Module called edgar_downloader, consists of 2 functions:
1. write_page(url, file_path)
    This will take in a URL and write the html to path specified
2. download_files_10k(ticker, dest_folder)
    Downloads all html 10-k files to dest_folder. 
    Convention: "<ticker>_10-k_<filing_date>.html"
Follow with Unit tests

## Part 1 - Data Preparation / Cleaning
Module called edgar_cleaner. The module should contain the following functions: 
1 clean_html_text(html_text)
Takes in a html text string and removes tags and special characters. Returns result as a string.
2 write_clean_html_text_files(input_folder, dest_folder)
Takes all the html 10-k files in the input folder, cleans them using the clean_html_text function 
and writes them into the destination folder as text files. Files downloaded should follow the 
naming convention: <ticker>_10-k_<filing_date>.txt.

Follow with units
## Step 3

## Step 4

## Post-Pipeline
