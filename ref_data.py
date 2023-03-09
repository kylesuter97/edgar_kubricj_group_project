import requests
from bs4 import BeautifulSoup
import re
import yahoofinancials
from yahoofinancials import YahooFinancials
import pandas as pd
import numpy as np
import os


def get_sp100():
    
    url = r'https://en.wikipedia.org/wiki/S%26P_100'
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser') 

    tag = 'table'
    attributes = {'id':'constituents'}    
    table_soup = soup.find(tag, attributes)  

    table_data = []
    for row in table_soup.find_all('tr'):
        row_text = [i.text.strip() for i in row.find_all('td')]
        table_data.append(row_text)

    ticker_list = []
    for i in table_data:
        if len(i) > 0:
            ticker_list.append(i[0])

    for index in range(len(ticker_list)):
        if '.' in ticker_list[index]:
            ticker_list[index] = ticker_list[index].replace('.', '-')

    return ticker_list


def get_yahoo_data(start_date: str,end_date: str,tickers: list=get_sp100(),time_period: str='daily'):
    prices_list=[]
    data = YahooFinancials(tickers).get_historical_price_data(start_date, end_date, time_period)
    for ticker in tickers:
        for item in data[ticker]['prices']:
            item['symbol']=ticker
        prices_list = prices_list + data[ticker]['prices']
    
    df = pd.DataFrame(prices_list)

    df.drop(columns = ['open', 'close','date'], inplace = True)

    df.rename(columns={'adjclose':'price'},inplace=True)

    df['formatted_date'] = pd.to_datetime(df['formatted_date'])

    df.rename(columns={'formatted_date':'date'},inplace=True)
    df['1daily_return']=df.groupby('symbol')['price'].pct_change(periods=1).shift(-1)
    df['2daily_return']=df.groupby('symbol')['price'].pct_change(periods=2).shift(-2)
    df['3daily_return']=df.groupby('symbol')['price'].pct_change(periods=3).shift(-3)
    df['5daily_return']=df.groupby('symbol')['price'].pct_change(periods=5).shift(-5)
    df['10daily_return']=df.groupby('symbol')['price'].pct_change(periods=10).shift(-10)

    df=df[['date','high','low','price','volume','1daily_return','2daily_return','3daily_return','5daily_return','10daily_return','symbol']]

    return df



def get_sentiment_word_dict():
    # Define the path of the file containing the sentiment word data
    # os.chdir(r"C:\\Users\\Nixon Ng\\OneDrive - Kubrick Group\\Desktop\\Kubrick Training Program\\Week 10 (Edgar)\\edgar_project\\edgar-bps")
    # filename = rf'../edgar-bps/lm_dict_1993-2021.csv'    
    cwd = os.getcwd()
    os.chdir(cwd)
    filename = os.fsdecode('lm_dict_1993-2021.csv')
    # Create the dictionary containing sentiments as dictionary keys, and list of sentiment words as dictionary values    
    sentiment_dict = {'Positive': [], 'Negative': [], 'Uncertainty': [], 'Litigious': [], 
                      'Strong Modal': [], 'Weak Modal': [], 'Constraining': [], 'Superfluous': [], 
                      'Interesting': [], 'Modal': []}
    # Read the csv file using pandas
    lm_df = pd.read_csv(filename)
    # Optional: Remove rows for non-essential columns    
    # lm_df = lm_df.drop(columns = ['Seq_num','Word Count','Word Proportion','Average Proportion','Std Dev','Doc Count','Syllables','Source'])
    # Create the filters for each dictionary key    
    mask1 = lm_df['Positive'] > 0 
    mask2 = lm_df['Negative'] > 0
    mask3 = lm_df['Uncertainty'] > 0
    mask4 = lm_df['Litigious'] > 0
    mask5 = lm_df['Strong_Modal'] > 0
    mask6 = lm_df['Weak_Modal'] > 0
    mask7 = lm_df['Constraining'] > 0
    # Integrate the filters to create new dataframes    
    sentiment_word_df1 = lm_df[mask1]
    sentiment_word_df2 = lm_df[mask2]
    sentiment_word_df3 = lm_df[mask3] 
    sentiment_word_df4 = lm_df[mask4] 
    sentiment_word_df5 = lm_df[mask5]
    sentiment_word_df6 = lm_df[mask6]
    sentiment_word_df7 = lm_df[mask7]
    # Using new dataframes, for loop is used to append the words into the sentiment dictionary
    for row_dict in sentiment_word_df1.to_dict(orient='records'):
        sentiment_dict['Positive'].append(row_dict['Word'])
    for row_dict in sentiment_word_df2.to_dict(orient='records'):
        sentiment_dict['Negative'].append(row_dict['Word'])
    for row_dict in sentiment_word_df3.to_dict(orient='records'):
        sentiment_dict['Uncertainty'].append(row_dict['Word'])
    for row_dict in sentiment_word_df4.to_dict(orient='records'):
        sentiment_dict['Litigious'].append(row_dict['Word'])
    for row_dict in sentiment_word_df5.to_dict(orient='records'):
        sentiment_dict['Strong Modal'].append(row_dict['Word'])
    for row_dict in sentiment_word_df6.to_dict(orient='records'):
        sentiment_dict['Weak Modal'].append(row_dict['Word'])
    for row_dict in sentiment_word_df7.to_dict(orient='records'):
        sentiment_dict['Constraining'].append(row_dict['Word'])
    # Return the dictionary of sentiment words    
    return sentiment_dict