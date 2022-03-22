from zoneinfo import available_timezones
import requests
import json
import os.path
import pickle
from steamget import get_item
from bs4 import BeautifulSoup
from htmgeny import htmlgen
from urlextractor import *
from begin import basic
scapper=basic()
visited=scapper.visited
failedlinks=scapper.failedlinks
match_string=scapper.match_string
remove_string=scapper.remove_string
url=scapper.urls
data=scapper.data
data_keys=scapper.data_keys

steamlink={}   
devianturls=set()                                                             
new={}
newhtmldict={}

#stores page data in the url[]  links only like www.deviantart.com/ artist name /art/ artwork name
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
    while NextBtnClicker<=2 and nexts:
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
print(f"Links extracted ={len(devianturls)}\n Accessing {len(availablelinks)} links...")                                                             
for artworkurls in availablelinks:
        print("Accessing ArtWork page "+ artworkurls)
        visited.add(artworkurls)
        page = requests.get(artworkurls)  
        soup = BeautifulSoup(page.content, 'html.parser')                    
        for pagedata in soup.findAll('a',{'class':"external"}):
            hrefval=pagedata.get('href')                                    
            if match_string in hrefval:                                       #match string has the steammarket link
                hrefval=remove_filter(hrefval)
                steamlink.add(hrefval.replace(remove_string,""))           #deviant external link is stripped and if matches its added into this set
                                            

print(f"{len(steamlink)} steam links extracted")
#DUplicate remover not nessary for steam links as price might change
# c=0
# if(len(steamlink)>0):
#     for steamlinks in data_keys:                                                  # if Url is previously stored in .json this removes it from the current steamlink[]
#         try:
#             steamlink.remove(steamlinks)
#         except ValueError:
#             c+=1
#     print(str(c)+" Duplicates have been removed")
print("\n\n\nIF program Breakes \n")
print(10*'#'+"copy from '[' \n∨∨∨∨∨")
print(steamlink)
print(10*'#'+"Till the end of braces ']' ^^^^^^^")

for link in steamlink:
    try:
        price=get_item(link)
        if(not "NA" in price ):
            price=price.replace('₹','').replace(',','')
            price=float(price)
            if(price >=60.00):                                                 #Appends only if value is greater than 60
                new[link]=price
                data[link]=price
            #data now has merged data from file and new appends to it 
            # Finally writing the data to file
            with open('new.json',"w",encoding='utf-8') as json_file:           
                json_file.write(json.dumps(new))
    except TypeError: 
        failedlinks.append(link)
        print(link+"failed ")
        pass
with open('data.json',"w",encoding='utf-8') as json_file:                      
    json_file.write(json.dumps(data))
with open('failed.pkl', "wb") as txtfile:                                        # Pickling the final links to file
    pickle.dump(failedlinks, txtfile)
failedlinks=list(set(failedlinks))
with open('links.pkl', "wb") as txtfile:                                        # Pickling the final links to file
    pickle.dump(visited, txtfile)
for links in steamlink:
    print(links)

import rerunner
rerunner