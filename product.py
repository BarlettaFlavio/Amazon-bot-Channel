

import fake_useragent
import selectorlib 
from selectorlib import Extractor
import requests
from fake_useragent import UserAgent

import json
from time import sleep


# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('products2.yml')

def caption_creation(name,price_global,price_amazon,price_deal,url):
    
    caption=name+'\nPrezzo '
    
    if price_global is None:
        caption+=price_amazon
    elif price_deal is None:
        caption+='da '+price_global+' a '+price_amazon
    else:
        caption+='da '+price_global+' a '+price_deal
    
    caption+='\n'+u'\U0001F50E'+url
    return caption
            
def best_image(strimagelist):
    strimagelist=strimagelist.strip('{}\[]')
    img=strimagelist.split(',')
    l=len(img)
    max_img=0
    max_pos=0
    for i in range(1,l,2):
        img[i]=img[i].strip(']')
        if(max_img<int(img[i])):
            max_img = int(img[i])
            max_pos=i-1
        
    im=img[max_pos]
    return im[1:-6]
def scrape(url):

    ua = UserAgent()

 
    headers = {
        'authority': 'www.amazon.it',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': ua.random,
        #'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
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
 
    return e.extract(r.text)

# product_data = []
#with open("product_urls.txt",'r') as urllist, 
with open('product_output.jsonl','w', encoding='utf8') as outfile:
    #for url in urllist.read().splitlines():
    while(True):
        url=input('url ');
        data=None
        while(data is None):
            print("tentativo")
            data = scrape(url)
        print(data['category'])
        try:

            caption=caption_creation(data['name'],data['price_global'],data['price_amazon'],data['price_deal'],url)
            
            print('\n'+caption+'\n')
            json.dump(data,outfile, ensure_ascii=False)
            outfile.write("\n")
    
        except:
            json.dump(data,outfile, ensure_ascii=False)
            outfile.write("\n")
        
        im=best_image(data['image'])
        print(im)

