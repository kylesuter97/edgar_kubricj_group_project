import yahoofinancials
from yahoofinancials import YahooFinancials
import pandas as pd
import numpy as np

def get_yahoo_data(start_date: str,end_date: str,tickers: list,time_period: str='daily'):
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
