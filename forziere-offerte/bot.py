# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 12:35:27 2020
https://aqueous-atoll-80142.herokuapp.com/1338925720:AAGTfxJbjRM7QXEImJYzreJKws5qh-YIKsk
@author: Flavio #cID=message.chat.id    bot.send_photo(cID,image,text)
"""
import fake_useragent
import selectorlib 
from selectorlib import Extractor
import requests
import os
#from fake_useragent import UserAgent
from flask import Flask, request



# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('products.yml')

def scrape(url):

    #ua = UserAgent()

    headers = {
        'authority': 'www.amazon.it',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        #'user-agent': ua.random,
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        #'sec-fetch-site': 'same-origin','sec-fetch-user': '?1',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'it-IT,en-GB,en-US;q=0.9,en;q=0.8',
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


import telebot

chatidChannel='@testingflavio'
caption='error'

TOKEN = '1338925720:AAGTfxJbjRM7QXEImJYzreJKws5qh-YIKsk'
bot = telebot.TeleBot(token=TOKEN)
server = Flask(__name__)
regex="(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://forziere-offerte-amazon.herokuapp.com/' + TOKEN)
    return "!", 200

#COMANDI

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@bot.message_handler(func=lambda msg: msg.text)
#@bot.message_handler(regexp=regex)
def amazon_scrape(message):
    caption='error'
    url=message.text
    data=None
    while(data is None):
        print("tentativo")
        data = scrape(url)
    
    print(data)
    if data:
        try:
            img=data["image"].split(':[')
            image=img[0].strip('{"')
            
            caption=data['name']+'\n'+'Prezzo '
            
            if data['price_global'] is None:
                caption+=data['price_amazon']
            elif data['price_deal'] is None:
                caption+='da '+data['price_global']+' a '+data['price_amazon']
            else:
                caption+='da '+data['price_global']+' a '+data['price_deal']
            
            caption+'\n'+u'\U0001F50E'+url
            bot.reply_to(message,'ok')
            bot.send_photo(chatidChannel,image,caption)
        except:
            bot.reply_to(message,caption)



if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))