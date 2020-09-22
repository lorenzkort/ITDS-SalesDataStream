import requests
import io
from bs4 import BeautifulSoup as bs
import json
import pandas as pd
import numpy as np
from telegram_bot import telegram_send_text

def get_url(keyword):
    url = 'https://www.careerguide.nl/zoek-vacatures/?t=' + str(keyword).replace(' ', '%20') + '&t2=&n=&o=&e=&r='
    return url

def get_soup(url):
    page = requests.get(url).text
    soup = bs(str(page), 'html.parser')
    return soup

def get_itemlinks(soup):
    soup = soup.find('div')
    item_id = 0
    item_list = ''
    while True:
        item = soup.find('a', {'id':'ContentPlaceHolder1_lvVacatures_hlVacature_'+ str(item_id)})
        if item == None:
            break
        item_list = item_list + str(item)
        item_id = item_id + 1
    soup = bs(item_list, features="html.parser")
    item_links = ['https://www.careerguide.nl' + a['href'] for a in soup.find_all('a', href=True)]
    return item_links

def create_df(keyword='Data Steward'):
    url = get_url(keyword)
    soup = get_soup(url)
    item_links = get_itemlinks(soup)
    df = pd.DataFrame({'keyword':keyword,'url':item_links})
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

def check_careerguide(keyword='Data Steward', chat_id='-459671235'):
    dir = 'data/' # @Windows
    #dir = '/home/pi/Documents/Python/ITDS/data/' # @raspberyPi
    file_name = dir + 'CareerGuide_' + keyword.replace(' ','_').lower() + '_response.csv'
    items_df = create_df(keyword) # get items
    try:
        notify(items_df, file_name, keyword, chat_id) # mail new id's
    except:
        print('No saved file found')
    items_df.to_csv(file_name) # save csv
    return