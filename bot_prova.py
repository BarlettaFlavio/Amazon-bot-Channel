# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 12:35:27 2020

@author: Flavio #cID=message.chat.id    bot.send_photo(cID,image,text)
"""
import fake_useragent
import selectorlib 
from selectorlib import Extractor
import requests
from fake_useragent import UserAgent

import json
from time import sleep

# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('products2.yml')

def scrape(url):

    ua = UserAgent()


    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': ua.random,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-charset': 'utf-8, iso-8859-1;q=0.5',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.it/',
        'accept-language': 'it-IT;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    print(r)
    return e.extract(r.text)

import time
import telebot

chatidChannel='@testingflavio'
caption='error'

TOKEN = '1338925720:AAGTfxJbjRM7QXEImJYzreJKws5qh-YIKsk'
bot = telebot.TeleBot(token=TOKEN)

regex="(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"

@bot.message_handler(func=lambda msg: msg.text)
#@bot.message_handler(regexp=regex)
def amazon_scrape(message):
    caption='error'
    url=message.text
    data=""
    print(data)
    data = scrape(url) 
    
    print(data)
    if data:
        try:
            img=data["image"].split(':[')
            image=img[0].strip('{"')
            
            
            if data['price_global'] is None:
                caption=data['name']+'\n'+'Prezzo '+data['price_amazon']+'\n'+u'\U0001F50E'+url
            elif data['price_deal'] is None:
                caption=data['name']+'\n'+'Prezzo da '+data['price_global']+' a '+data['price_amazon']+'\n'+u'\U0001F50E'+url
            else:
                caption=data['name']+'\n'+'Prezzo da '+data['price_global']+' a '+data['price_deal']+'\n'+u'\U0001F50E'+url
            
            bot.reply_to(message,'ok')
            bot.send_photo(chatidChannel,image,caption)
        except:
            bot.reply_to(message,caption)
while True:
    try:
        bot.polling(none_stop=True)
        # ConnectionError and ReadTimeout because of possible timout of the requests library
        # maybe there are others, therefore Exception
    except Exception:
        time.sleep(15)