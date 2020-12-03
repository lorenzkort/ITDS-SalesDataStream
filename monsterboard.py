from pathlib import Path
import os, requests, copy
from bs4 import BeautifulSoup as bs
import json
import pandas as pd
import numpy as np
from telegram_bot import telegram_send_text

def get_url(keyword):
    url = 'https://www.monsterboard.nl/vacatures/zoeken/?q=' + str(keyword).replace(' ', '-') + '&tm=7&cy=nl&tm=30&page=10'
    return url

def get_path(keyword):
    #dir = 'data/' # @Windows
    dir = '/home/pi/Documents/Python/ITDS/data/' # @raspberyPi
    filename = Path(dir + 'monsterboard_' + keyword.replace(' ','_').lower() + '_response.csv')
    if not filename.exists():
        open(filename, 'w+').close()
    return filename

def get_soup(url):
    page = requests.get(url).text
    soup = bs(str(page), 'html.parser')
    return soup

def get_listings(soup):
    soup = soup.find_all('div', class_='summary')
    items = [item.find('h2', class_='title').find('a', href=True)['href'].encode('Latin-1', 'ignore').decode('Latin-1') for item in soup if item.find('h2', class_='title') is not None]
    return items

def create_df(keyword):
    url = get_url(keyword)
    soup = get_soup(url)
    items = sorted(get_listings(soup))
    df = pd.DataFrame(items, columns=['url']).drop_duplicates()
    return df

def notify(df, keyword, chat_id='-425371692'):
    return [telegram_send_text(f'Keyword "{keyword}":\n {url}') for url in df['url']]
    

def get_new_items(new_df, keyword):
    try:
        old_df = pd.read_csv(get_path(keyword)) #try getting file
        old_df = old_df[['url']]
        new_items = new_df.assign(Inold_df=new_df.url.isin(old_df.url).astype(int))
        new_items = new_items[new_items['Inold_df']==0]
        return new_items
    except:
        print('Failed to convert existing file to pandas dataframe')
    return

def check_monsterboard(keyword='Data', chat_id='-459671235'):
    response_df = create_df(keyword) # get items
    new_items = get_new_items(response_df, keyword) # mail new id's
    if len(new_items.index) > 0:
        notify(new_items, keyword)
    response_df.to_csv(get_path(keyword)) # save csv
    return new_items

if __name__ == "__main__":
    check_monsterboard()
    