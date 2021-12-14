from bs4 import BeautifulSoup
import requests
import json
from json2html import *
import os 
import os.path
from htmgeny import htmlgen
from urlextractor import urlextractor
import pickle
from steamget import get_item

def clear():
  _ = os.system('clear') if os.name == 'posix' else  os.system('cls')
#Checking for files
if (not os.path.isfile('links.pkl')):
    with open('links.pkl', 'wb') as fp:
        nam=["Blank","Blank1"]
        pickle.dump(nam, fp)
if (not os.path.isfile('data.json')):
    with open('data.json', 'w') as fp:
        fp.write(json.dumps({"LINKS": "values"}))
#pickling to load previous data
onlylinks=[]
with open('links.pkl', "rb") as txtfile:
    onlylinks = pickle.load(txtfile)
with open('data.json') as json_file:  
    data = json.load(json_file)                                               #has the data from prev searches stored in this 
devianturls=[]                                                                #consists of all deviant urls

steamlink=[]   
new={}
newhtmldict={}
match_string="https://steamcommunity.com/market/listings/"
remove_string="https://www.deviantart.com/users/outgoing?"
#url[] stores all the urls to get art links from infiniteurl[] also has infinite scrollable pages to fix that 
url=[]
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
    print("Accessing Deviant gallery page "+ devianturl)
    devianturls=list(set(devianturls))                          
    NextBtnClicker = 0
    print("Current data "+str(len(devianturls)))
    nexts=urlextractor(devianturl)
    while NextBtnClicker<=10 and nexts[0]!=1:
        print(f"Accessing page {NextBtnClicker}....")
        nexts=urlextractor(devianturl+nexts[0])
        main_page = requests.get(devianturl)                                    
        soup = BeautifulSoup(main_page.content, 'html.parser')                                          
        for deviantdata in soup.findAll('a',{'data-hook':"deviation_link"}):
            hrefval=deviantdata.get('href')
            devianturls.append(hrefval)    
        NextBtnClicker+=1

devianturls=list(set(devianturls))   

print("Links extracted ="+str(len(devianturls)))                                      
#                                                                             #stores all the steam links                                                                        
for artworkurls in devianturls:
    if (artworkurls not in onlylinks):                                     #visiting each pages to check for steam link brute force*        
        print("Accessing ArtWork page "+ artworkurls)
        onlylinks.append(artworkurls)
        page = requests.get(artworkurls)  
        soup = BeautifulSoup(page.content, 'html.parser')                    
        for pagedata in soup.findAll('a',{'class':"external"}):
            hrefval=pagedata.get('href')                                    
            if match_string in hrefval:                                       #match string has the steammarket link
                steamlink.append(hrefval.replace(remove_string,""))           #deviant external link is stripped and if matches its added into this set
onlylinks=list(set(onlylinks))                                                
steamlink=list(set(steamlink))                                               
data_keys=data.keys()
print(str(len(steamlink))+" steam links extracted")
c=0
if(len(steamlink)>0):
    for steamlinks in data_keys:                                                  # if Url is previously stored in .json this removes it from the current steamlink[]
        try:
            steamlink.remove(steamlinks)
        except ValueError:
            c+=1
    print(str(c)+" Duplicates have been removed")

print(10*'#'+"copy from '[' \n∨∨∨∨∨")
print(steamlink)
print(10*'#'+"Till the end of braces ']' ^^^^^^^")
############################################## till here and pass the array of steam links to the next array##############################
#steamlink=[]
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
        print(link+"failed ")
        pass
with open('data.json',"w",encoding='utf-8') as json_file:                      
    json_file.write(json.dumps(data))

with open('links.pkl', "wb") as txtfile:                                        # Pickling the final links to file
    pickle.dump(onlylinks, txtfile)
for links in steamlink:
    print(links)
htmlgen("data.json")
htmlgen("new.json")
print("Check new.html For Latest data")