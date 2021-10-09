from bs4 import BeautifulSoup
import requests
import json
import time
from urllib.parse import unquote

from requests.api import get

match_string="https://steamcommunity.com/market/listings/"
remove_string="https://www.deviantart.com/users/outgoing?"
url2="https://steamcommunity.com/market/listings/753/"
appid=int(753)
url=["https://www.deviantart.com/tag/steamprofile?order=this-month","https://www.deviantart.com/tag/steamprofile?order=most-recent","https://www.deviantart.com/tag/steamprofile?order=this-week"]
main="https://www.deviantart.com/tag/steamprofiledesign?page="
#generates follow up urls for custom urls 
#recommended to run once 
for i in range(1,10):
    url.append(f'https://www.deviantart.com/tag/steamprofiledesign?page={str(i)}')
#url[] stores all the urls to get links from

with open('data.json') as json_file:
    data = json.load(json_file)                                             #has the data from prev searches stored in this 

#get_item(item_name ) should be non url encoded url like
# example get_item("https://steamcommunity.com/market/listings/753/746850-Chinatown" ) returns :₹ 269.36  ( {currency} value )
def get_item(item):
        item=item.replace(url2,"")
        market_hash_name= unquote(item)
        url = f'https://steamcommunity.com/market/priceoverview/?country=US&currency=24&appid={appid}&market_hash_name={market_hash_name}'
        time.sleep(2)
        resp = requests.get(url)
        try:
            if resp.ok:                     
                jsondata=json.loads(resp.content)
                if jsondata['success'] :                                    #if item exits  returns price
                    return jsondata["lowest_price"]
                else:
                    print(item +" has no value") 
            else:
                print(resp)
                print("going to sleep for 5 sec")
                time.sleep(5)
                get_item(item)
        except KeyError:
                return "NA"
alldata=[]                                                                   #stores page data in the url[]  links only like www.deviantart.com/ artist name /art/ artwork name
for i in url:
    print("Accessing Devient gallery page "+ i)                                     
    main_page = requests.get(i)                                             #accesss the pages
    soup = BeautifulSoup(main_page.content, 'html.parser')                                          
    for i in soup.findAll('a',{'data-hook':"deviation_link"}):
        hrefval=i.get('href')
        alldata.append(hrefval)                                                     
alldata=list(set(alldata))                                                  # duplicates removed
steamlink=[]                                                                #stores all the steam links 

#visiting each pages to check for steam link brute force*
for i in alldata:
    print("Accessing ArtWork page "+ i)
    page = requests.get(i)
    soup = BeautifulSoup(page.content, 'html.parser')                       #visiting each page and checking for href to steam market 
    for j in soup.findAll('a',{'class':"external"}):
        hrefval=j.get('href')                                               #href val holds all the links which are in the page
        if match_string in hrefval:                                         #match string has the steammarket link
            steamlink.append(hrefval.replace(remove_string,""))             #devient external link is stripped and if matches its added into this set
steamlink=list(set(steamlink))                                              #sorting
data_keys=data.keys()                                                       #gets all the links from file
# if Url is previously stored in .json this removes it from the current steamlink[]
for i in data_keys:
    try:
        steamlink.remove(data_keys)
    except ValueError:
        print(i+" already exists")

#sends each item to get its val and its stored in final

for i in steamlink:
    price=get_item(i)
    if(not "NA" in price ):
        price=price.replace('₹','')
        price=float(price)
        if(price >=150.00):                                                 #Appends only if value is greater than 150
            data[i]=price

#data now has merged data from file and new appends to it 
# Finally writing the data to file

with open('data.json',"w",encoding='utf-8') as json_file:
    json_file.write(json.dumps(data))