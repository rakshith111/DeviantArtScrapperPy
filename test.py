import requests
import json
import re

from libs.steamget import get_item
from bs4 import BeautifulSoup
from libs.htmgeny import htmlgen
from libs.urlextractor import *
from begin import scrapper
scapper=scrapper()
visited=scapper.visited
failedlinks=scapper.failedlinks
match_string=scapper.match_string
remove_string=scapper.remove_string
url=scapper.urls
data=scapper.data
data_keys=scapper.data_keys
latest=scapper.latest

steamlink=set()  
devianturls=set()                                                             
newhtmldict={}
availablelinks=set()


for devianturl in url:
    print("Accessing Deviant gallery page "+ devianturl)          
    NextBtnClicker = 1
    page=requests.get(devianturl)
    page_cookie=page.cookies
    soup = BeautifulSoup(page.content, 'html.parser')  
    for deviantdata in soup.findAll('a',{'data-hook':"deviation_link"}):
            hrefval=deviantdata.get('href')
            devianturls.add(hrefval)
    nexts=urlextractor(devianturl,page_cookie)
    while NextBtnClicker<=1 and nexts:                                                              #Change 2 to any number less than 5 after inital run
        print(f"Accessing page {NextBtnClicker}....")
        joinedurl=devianturl+"&"+nexts
        main_page = requests.get(joinedurl,cookies=page_cookie)
        mp_cookie=main_page.cookies     
        soup = BeautifulSoup(main_page.content, 'html.parser')                                          
        for deviantdata in soup.findAll('a',{'data-hook':"deviation_link"}):
            hrefval=deviantdata.get('href')
            devianturls.add(hrefval)
        nexts=urlextractor(joinedurl,mp_cookie)
        NextBtnClicker+=1
        sleep(2)
availablelinks=devianturls-visited   
print(f"Links extracted ={len(devianturls)} \nAccessing {len(availablelinks)} links...")                                                             
for artworkurls in availablelinks:
        #print("Accessing ArtWork page "+ artworkurls)
        visited.add(artworkurls)
        page = requests.get(artworkurls)  
        soup = BeautifulSoup(page.content, 'html.parser')                    
        for pagedata in soup.findAll('a',{'class':"external"}):
            hrefval=pagedata.get('href')                                    
            if match_string in hrefval:                                       #match string has the steammarket link
                hrefval=remove_filter(hrefval)
                steamlink.add(hrefval.replace(remove_string,""))              #deviant external link is stripped and if matches its added into this set
                                            
print(f"{len(steamlink)} steam links extracted")

with open ("laststeam.txt","w") as f:
    json.dump(list(steamlink),f)
print("Current Steam links saved to file : laststeam.txt \nRun it with another prog if the script breaks ")
for link in steamlink:
    try:
        price=get_item(link)
        if(not "NA" in price ):
            price=float(re.findall("[\d]+.[\d]+",price)[0])
            if(price >=100.00):                                                 #Appends only if value is greater than 100
                latest[link]=price
                data[link]=price
            #data now has merged data from file and new appends to it 
            # Finally writing the data to file
    except TypeError: 
        failedlinks.append(link)
        print(link+" failed ")
        pass
scapper.writer()
scapper.rerunner()