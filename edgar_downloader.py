from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import pandas as pd

def write_page(url, file_path):
    driver = webdriver.Chrome()

    #Load EDGAR website
    driver.get(url)
    time.sleep(1)#Sleep to allow it to run

    #get filing date for later
    xpath_filing_date = r'//*[@id="formDiv"]/div[2]/div[1]/div[2]'
    global filingdate
    filingdate = driver.find_element("xpath", xpath_filing_date).text

    #Link to html file
    xpath_ixbrl = r'//*[@id="formDiv"]/div/table/tbody/tr[2]/td[3]/a'
    driver.find_element("xpath", xpath_ixbrl).click()
    time.sleep(1)

    #If HTML+CSS, proceed to "Open as HTML", otherwise assume already HTML
    try:
        #clicks on the menu button if present
        xpath_menu = r'//*[@id="menu-dropdown-link"]/i'
        driver.find_element("xpath", xpath_menu).click()
        #clicks Open as Html
        xpath_final = r'//*[@id="form-information-html"]'
        driver.find_element("xpath", xpath_final).click()
        driver.switch_to.window(driver.window_handles[1])
    except Exception:
        pass
    time.sleep(3)
    #create output file path
    tempfile_name = "thistempfile.html"


    #Output to path
    try:
        with open(tempfile_name, "w", encoding='utf-8') as f:
            f.write(driver.page_source)
            return filingdate

    except FileExistsError:
        print("One of the files already exists, please remove it")

def download_files_10k(ticker, dest_folder):
    #Saves varaible with local dir
    cwd = os.getcwd()

    #Sets up webdriver to save files to local dir
    options = webdriver.ChromeOptions() 
    prefs = {"download.default_directory" : cwd}

    #example: prefs = {"download.default_directory" : "C:\Tutorial\down"};
    options.add_experimental_option("prefs",prefs)

    #Creates driver object
    driver = webdriver.Chrome(options=options)

    #Load EDGAR website
    driver.get(r'https://www.sec.gov/edgar/searchedgar/companysearch')
    time.sleep(1)#Sleep to allow it to run

    #Xpath to search box on edgar
    xpath_search_box = r'//*[@id="edgar-company-person"]'

    #Send the keystroke for requested 'ticker' followed by enter key to searchbox
    driver.find_element("xpath", xpath_search_box).send_keys(ticker, Keys.ENTER)
    time.sleep(1 #Sleep to allow it to run

    #Now we need to click on "10-K (annual reports)..." to expand collapsible
    xpath_10k_expand = r'//*[@id="filingsStart"]/div[2]/div[3]/h5'
    driver.find_element("xpath", xpath_10k_expand).click()
    time.sleep(1) #Sleep to allow it to run

    #Now click on "View all 10-ks and 10-Qs"
    xpath_10k_all= r'//*[@id="filingsStart"]/div[2]/div[3]/div/button[1]'
    driver.find_element("xpath", xpath_10k_all).click()
    time.sleep(1) #Sleep to allow it to run

    #Enter "10-k" in search box and then end
    #Send the keystroke for requested 'ticker' followed by enter key to searchbox
    xpath_filings = r'//*[@id="searchbox"]'
    driver.find_element("xpath", xpath_filings).send_keys("10-k", Keys.ENTER)
    time.sleep(1) #Sleep to allow it to run

    #Deletes any previously downloaded edgar files that might crash the script
    try:
        os.remove("EDGAR Entity Landing Page.xlsx")
    except OSError:
        pass

    #Downloads  excel to get links to all filings
    xpath_filings_excelbutton = r'//*[@id="filingsTable_wrapper"]/div[1]/button[3]'
    driver.find_element("xpath", xpath_filings_excelbutton).click()
    time.sleep(1) #Sleep to allow it to run

    #Closes driver
    driver.close()

    #renames file name to ticker_edgar_filings.xlsx, deletes if exists
    temp_file_name = f"{ticker}_edgar_filings.xlsx"
    try:
        os.rename("EDGAR Entity Landing Page.xlsx", temp_file_name)    
    except FileExistsError:
        os.remove(temp_file_name)
        os.rename("EDGAR Entity Landing Page.xlsx", temp_file_name)

    #import to pandas df
    filings_raw_df = pd.read_excel(temp_file_name)

    #Drop unneeded columns and rename last to url
    cleaned_df = filings_raw_df.drop(columns=["EDGAR Entity Landing Page", "Unnamed: 1", "Unnamed: 2","Unnamed: 3"])

    #rename column, drop first 2 rows and missing values, reset index
    cleaned_df = cleaned_df.rename(columns=cleaned_df.iloc[1])
    cleaned_df = cleaned_df.drop([0,1])
    cleaned_df = cleaned_df.dropna(axis = 0) #
    cleaned_df.reset_index(drop=True, inplace=True)

    #Outputs list of all rls
    list_of_urls = cleaned_df["Filings URL"].values.tolist()

    #Delete excel file after done
    try:
        os.remove(temp_file_name)    
    except FileNotFoundError:
        pass

    #run through each url in list with write_page function, THEN RENAMES
    for iurl in list_of_urls:
        write_page(iurl, dest_folder)
        #rename files
        file_name = '\\' + ticker + "_10-k_" + filingdate + ".html"
        final_name = rf"{dest_folder}{file_name}"
        
        try:
            os.rename("thistempfile.html", final_name)    
        except FileExistsError:
            os.remove(final_name)
            os.rename("thistempfile.html", final_name)

    #If made it to the end, print all files saved
    print("All 10k's have been saved at location")