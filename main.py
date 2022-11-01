# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 16:00:42 2022

@author: sareman
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError
import requests
import lxml
import pandas as pd
from time import sleep
import json

list_card_url=[]
resultall=[]
full_name=[]
full_tel=[]
full_edr=[]

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

for page in range(1,150):
    sleep(2)
    url = f'https://graintrade.com.ua/proizvoditeli?User_page={page}'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    data = soup.find_all ('div', {'class':'companyTitle'})
    
    for i in data:
        card_url="https://graintrade.com.ua" + i.find('a').get('href')
        list_card_url.append(card_url)
    

for card_url in list_card_url:
    
    response=requests.get(card_url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    data= soup.find ('div', {'class':'infoout'})
    name=data.find('b').text
    sel = data.select('b')

    try:
        comp_name =sel.pop(0).text
        others = sel.pop(1).text
        tel = sel.pop(1).text
        del sel[0], sel[0]
        edr =sel.pop(0).text

    except IndexError:
        comp_name='N/D'
        others='N/D'
        tel='N/D'
        edr='N/D'
        continue
    
    full_name.append(comp_name)
    full_tel.append(tel)
    full_edr.append(edr)

def Convert(o_list, t_list):
    o_l=iter(o_list)
    t_l=iter(t_list)
    result=dict(zip(o_l, t_l))
    return result

list5=Convert(full_name, full_edr)
list6=Convert(full_name, full_tel)

print(list5, list6)
   
with open('data46.txt', 'w',  encoding='utf-8') as f:
    for lists in list5:
        f.write(lists)
        f.write('\n')
with open('data46_1.txt', 'w', encoding='utf-8') as f:
    for lists1 in list6:
        f.write(lists1)
        f.write('\n')

json_file=json.dumps(list5)
f=open("file150.json", "x")
f.write(json_file)
f.close()
    
  