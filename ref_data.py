
import requests
from bs4 import BeautifulSoup
import re


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
        ticker_list[index] = re.sub(r'[^A-Za-z0-9]', '', ticker_list[index].upper())

    return ticker_list



