from bs4 import BeautifulSoup
import requests
import json
from json2html import *
import os 
import os.path
from htmgeny import htmlgen
import pickle
from time import sleep
from steamget import get_item
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.remote_connection import LOGGER, logging
LOGGER.setLevel(logging.WARNING)
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
alldata=[] 
steamlink=[]   
new={}
newhtmldict={}
match_string="https://steamcommunity.com/market/listings/"
remove_string="https://www.deviantart.com/users/outgoing?"

#############################################################comment from here#####################################################
#                                                                              #url[] stores all the urls to get art links from infiniteurl[] also has infinite scrollable pages to fix that 
infiniteurl=["https://www.deviantart.com/tag/steamprofile","https://www.deviantart.com/tag/steamartwork","https://www.deviantart.com/tag/steamshowcaseprofile","https://www.deviantart.com/tag/steamprofiledesigns","https://www.deviantart.com/tag/steamprofile?order=most-recent"]
driver = webdriver.Chrome(ChromeDriverManager().install())
for devianturl in infiniteurl:
    print("Accessing Devient gallery page "+ devianturl)                        
    driver.maximize_window()
    driver.get(devianturl)                                                    
    pagedata=driver.page_source 
    ScrollNumber = 8
    while ScrollNumber!=0:
        driver.execute_script("window.scrollTo(1,document.body.scrollHeight)")  #Scrolls to the bottom of the page 
        ScrollNumber-=1
        sleep(3)
    sleep(4)                                                                    
    pagedata=driver.page_source                                                
    soup = BeautifulSoup(pagedata,'html.parser')                                   #Parsing the htmldata to get required links 
    for deviantdata in soup.findAll('a',{'data-hook':"deviation_link"}):
        hrefval=deviantdata.get('href')
        alldata.append(hrefval)               
driver.close() 
print("Links extracted ="+str(len(alldata)))
alldata=list(set(alldata))  

url=["https://www.deviantart.com/tag/steamprofile?order=this-week","https://www.deviantart.com/tag/steamprofiledesigns?order=this-week","https://www.deviantart.com/tag/steamprofile?order=this-month"]

main="https://www.deviantart.com/tag/steamprofiledesign?page="
#generates follow up urls for custom urls 
#recommended to run once 
# for i in range(1,10):
#   url.append(f'https://www.deviantart.com/tag/steamprofiledesign?page={str(i)}')
#                                                                            #stores page data in the url[]  links only like www.deviantart.com/ artist name /art/ artwork name
for devianturl in url:
    print("Accessing Devient gallery page "+ devianturl)                                     
    main_page = requests.get(devianturl)                                    
    soup = BeautifulSoup(main_page.content, 'html.parser')                                          
    for deviantdata in soup.findAll('a',{'data-hook':"deviation_link"}):
        hrefval=deviantdata.get('href')
        alldata.append(hrefval)                                                     
alldata=list(set(alldata))                                                   
#                                                                             #stores all the steam links                                                                        
for artworkurls in alldata:
    if (not ( artworkurls in onlylinks)):                                     #visiting each pages to check for steam link brute force*        
        print("Accessing ArtWork page "+ artworkurls)
        onlylinks.append(artworkurls)
        page = requests.get(artworkurls)  
        soup = BeautifulSoup(page.content, 'html.parser')                    
        for pagedata in soup.findAll('a',{'class':"external"}):
            hrefval=pagedata.get('href')                                    
            if match_string in hrefval:                                       #match string has the steammarket link
                steamlink.append(hrefval.replace(remove_string,""))           #devient external link is stripped and if matches its added into this set
onlylinks=list(set(onlylinks))                                                
steamlink=list(set(steamlink))                                               
data_keys=data.keys()                                                         #gets all the links from file

for i in data_keys:                                                           # if Url is previously stored in .json this removes it from the current steamlink[]
    try:
        steamlink.remove(i)
    except ValueError:
        print(i+" Already exists")
clear()
clear()
clear()
print(10*'#'+"copy from '[' \n∨∨∨∨∨")
print(steamlink)
print(10*'#'+"Till the end of braces ']' ^^^^^^^")
############################################## till here and pass the array of steam links to the next array##############################
#steamlink=[]
for links in steamlink:
    try:
        price=get_item(links)
        if(not "NA" in price ):
            price=price.replace('₹','').replace(',','')
            price=float(price)
            if(price >=120.00):                                                 #Appends only if value is greater than 120
                new[links]=price
                data[links]=price
            #data now has merged data from file and new appends to it 
            # Finally writing the data to file
            with open('new.json',"w",encoding='utf-8') as json_file:           
                
                json_file.write(json.dumps(new))
    except TypeError: 
        print(links+"failed ")
        pass
with open('data.json',"w",encoding='utf-8') as json_file:                      
    json_file.write(json.dumps(data))

with open('links.pkl', "wb") as txtfile:                                        # Pickling the final links to file
    pickle.dump(onlylinks, txtfile)
htmlgen("data.json")
htmlgen("new.json")
clear()
clear()
clear()
print("Check new.html For Latest data")
