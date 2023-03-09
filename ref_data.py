import requests
from bs4 import BeautifulSoup
import re
import yahoofinancials
from yahoofinancials import YahooFinancials
import pandas as pd
import numpy as np


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