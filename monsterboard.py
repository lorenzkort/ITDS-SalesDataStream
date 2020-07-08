import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np
from telegram_bot import telegram_send_text

def get_url(keyword):
    url = 'https://www.monsterboard.nl/vacatures/zoeken/?q=' + str(keyword).replace(' ', '-') + '&cy=nl'
    return url

def get_soup(url):
    page = requests.get(url).text
    soup = BeautifulSoup(str(page), 'html.parser')
    return soup

def get_itemlinks(soup):
    soup = soup.find('div', {'class': 'scrollable'})
    soup = soup.find('script',{'type': 'application/ld+json'}).contents
    soup = json.loads(soup[0])
    return soup

def create_df(keyword='Data Analyst'):
    url = get_url(keyword)
    soup = get_soup(url)
    jresponse = get_itemlinks(soup)
    jresponse = [str(i['url']).replace(u'\u2013', '-').replace(u'\u2014', '-') for i in jresponse["itemListElement"]]
    df = pd.DataFrame({'keyword':keyword,'url':jresponse})
    df['url'].replace('', np.nan, inplace=True)
    df.dropna(subset=['url'], inplace=True)
    df['url']
    return df

def notify(df, file_name, keyword, chat_id='-425371692'):
    with open(file_name, 'r') as f:
        for ind in df.index:
            if any(df['url'][ind] in line for line in f):
                pass # known id
            else:
                print('New ' + keyword + ':' + df['url'][ind])
                telegram_send_text('Nieuwe vacature met keyword "' + keyword + '": ' + df['url'][ind], chat_id)
                break
    return

def check(keyword='Data Steward', chat_id='-459671235'):
    #dir = 'data/' # @Windows
    dir = '/home/pi/Documents/Python/ITDS/data/' # @raspberyPi
    file_name = dir + 'Monsterboard_' + keyword.replace(' ','_').lower() + '_response.csv'
    try:
        items_df = create_df(keyword) # get items
        notify(items_df, file_name, keyword, chat_id) # mail new id's
    except:
        items_df = pd.DataFrame()
    items_df.to_csv(file_name) # save csv
    return

