from bs4 import BeautifulSoup
import requests
import json
from json2html import *
import os
from urlextractor import *
import os.path
from htmgeny import htmlgen
import pickle
from steamget import get_item

#Checking for files
if (not os.path.isfile('links.pkl')):
    with open('links.pkl', 'wb') as fp:
        init=["Blank","Blank1"]
        pickle.dump(init, fp)
if (not os.path.isfile('failed.pkl')):
    with open('failed.pkl', 'wb') as fp:
        init=["https://steamcommunity.com/market/listings/753/447850-Void","https://steamcommunity.com/market/listings/753/554660-Puzzle%20Poker%20Card"]
        pickle.dump(init, fp)
if (not os.path.isfile('data.json')):
    with open('data.json', 'w') as fp:
        fp.write(json.dumps({"LINKS": "values"}))


#pickling to load previous data
onlylinks=[]
#url[] stores all the urls to get art links from infiniteurl[] also has infinite scrollable pages to fix that 
url=[]
failedlinks=[]
steamlink=[]   
devianturls=[]                                                                #consists of all deviant urls
new={}
newhtmldict={}

match_string="https://steamcommunity.com/market/listings/"
remove_string="https://www.deviantart.com/users/outgoing?"

with open('failed.pkl', "rb") as txtfile:
    failedlinks = pickle.load(txtfile)
with open('links.pkl', "rb") as txtfile:
    onlylinks = pickle.load(txtfile)
with open('data.json') as json_file:  
    data = json.load(json_file)                                               #has the data from prev searches stored in this 
data_keys=data.keys()

#generates follow up urls for custom urls 
mainurls=["https://www.deviantart.com/tag/steamprofile","https://www.deviantart.com/tag/steamprofiledesigns","https://www.deviantart.com/tag/steamartworkdesign","https://www.deviantart.com/tag/steamartwork","https://www.deviantart.com/tag/steamshowcaseprofile","https://www.deviantart.com/tag/steamprofiledesign"]
# for u in mainurls:
#     url.append(u+"?order=this-month")
#     url.append(u+"?order=this-week")
#     url.append(u+"?order=most-recent")
infiniteurl=["https://www.deviantart.com/tag/steamprofile","https://www.deviantart.com/tag/steamartwork","https://www.deviantart.com/tag/steamshowcaseprofile","https://www.deviantart.com/tag/steamprofiledesigns","https://www.deviantart.com/tag/steamprofile?order=most-recent"]

url+=infiniteurl
#stores page data in the url[]  links only like www.deviantart.com/ artist name /art/ artwork name
for devianturl in url:
    devianturls=list(set(devianturls))  
    print("Current data "+str(len(devianturls)))
    print("Accessing Deviant gallery page "+ devianturl)               
    NextBtnClicker = 1
    nexts=urlextractor(devianturl)
    while NextBtnClicker<=2 and nexts[0]!=1:
        print(f"Accessing page {NextBtnClicker}....")
        nexts=urlextractor(devianturl+nexts[0])
        main_page = requests.get(devianturl+nexts[0])                                    
        soup = BeautifulSoup(main_page.content, 'html.parser')                                          
        for deviantdata in soup.findAll('a',{'data-hook':"deviation_link"}):
            hrefval=deviantdata.get('href')
            devianturls.append(hrefval)    
        NextBtnClicker+=1

devianturls=list(set(devianturls))   

print("Links extracted ="+str(len(devianturls)))                           #stores all the steam links                                                                        
for artworkurls in devianturls:
    if (artworkurls not in onlylinks):                                     #visiting each pages to check for steam link , now only checks for previously non visited       
        print("Accessing ArtWork page "+ artworkurls)
        onlylinks.append(artworkurls)
        page = requests.get(artworkurls)  
        soup = BeautifulSoup(page.content, 'html.parser')                    
        for pagedata in soup.findAll('a',{'class':"external"}):
            hrefval=pagedata.get('href')                                    
            if match_string in hrefval:                                       #match string has the steammarket link
                hrefval=remove_filter(hrefval)
                steamlink.append(hrefval.replace(remove_string,""))           #deviant external link is stripped and if matches its added into this set

onlylinks=list(set(onlylinks))                                                
steamlink=list(set(steamlink))                                               

print(str(len(steamlink))+" steam links extracted")
c=0
if(len(steamlink)>0):
    for steamlinks in data_keys:                                                  # if Url is previously stored in .json this removes it from the current steamlink[]
        try:
            steamlink.remove(steamlinks)
        except ValueError:
            c+=1
    print(str(c)+" Duplicates have been removed")
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
    pickle.dump(onlylinks, txtfile)
for links in steamlink:
    print(links)

import rerunner