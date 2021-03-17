import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

def get_data(stock_code, year):
    r  = requests.get('https://www.poems.co.id/asp/stocks/research/HistoryValue.asp?a=CBDMIF&s=101323752156313.62&StockCode='+ stock_code + '&nYear=' + year)
    if r.status_code == 200:
        return r.text
    else:
        return ''

def get_year(stock_code):
    html = get_data(stock_code, '2020')
    soup = BeautifulSoup(html, 'html.parser')
    year_list = []
    for i in soup.find_all('option'):
        year_list.append(i.get('value'))
    return year_list

def add_to_dict(data_dict, name, value):
    if data_dict.get(name):
        data_dict[name].append(value)
    else:
        data_dict[name] = []
        data_dict[name].append(value)
    
    return data_dict

def convert_quarter(text):
    split_text = text.split('\xa0')
    switcher = {
        'March' : 'Q1',
        'June'  : 'Q2',
        'September' : 'Q3',
        'December'  : 'Q4'
    }
    q = switcher.get(split_text[0], '')
    return q+'-'+split_text[1]

def parse_number(str_number):
    if '.' in str_number:
        return float(str_number)
    else:
        return int(str_number)

def run_mining(stock_code):
    list_year = get_year(stock_code) 
    data_field = {}
    for i in list_year:
        html = get_data(stock_code, i)
        soup = BeautifulSoup(html, 'html.parser')
        for i in soup.find_all('table')[1].find_all('fieldset'):
            if i.legend:
                data_field = add_to_dict(data_field, 'Quarter', convert_quarter(i.legend.text))
                data_field = add_to_dict(data_field, 'Code', stock_code)
                for tr in i.find_all('tr'):
                    for td in tr.find_all('td'):
                        span = td.find_all('span')
                        if len(span) == 2:
                            data_field = add_to_dict(data_field, span[0].text, parse_number(span[1].text.replace(',','')))

    df_stock = pd.DataFrame(data_field)
    df_stock = df_stock.iloc[::-1].reset_index(drop=True)
    return df_stock