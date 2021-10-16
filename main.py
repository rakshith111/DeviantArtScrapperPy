from bs4 import BeautifulSoup
import requests
import json
import time
from urllib.parse import unquote
import os 
import os.path
import pickle
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.remote_connection import LOGGER, logging
LOGGER.setLevel(logging.WARNING)
def clear():
  _ = os.system('clear') if os.name == 'posix' else  os.system('cls')
alldata=[] 
steamlink=[]   
onlylinks=[]
new={}
appid=int(753) 
match_string="https://steamcommunity.com/market/listings/"
remove_string="https://www.deviantart.com/users/outgoing?"
url2="https://steamcommunity.com/market/listings/753/"
#                                                                              #url[] stores all the urls to get art links from infiniteurl[] also has infinite scrollable pages to fix that 
infiniteurl=["https://www.deviantart.com/tag/steamprofile","https://www.deviantart.com/tag/steamartwork","https://www.deviantart.com/tag/steamshowcaseprofile","https://www.deviantart.com/tag/steamprofiledesigns","https://www.deviantart.com/tag/steamprofile?order=most-recent"]

driver = webdriver.Chrome(ChromeDriverManager().install())
for devianturl in infiniteurl:
    print("Accessing Devient gallery page "+ devianturl)                        
    driver.maximize_window()
    driver.get(devianturl)                                                      #Opens the page
    pagedata=driver.page_source 
    ScrollNumber = 8
    while ScrollNumber!=0:
        driver.execute_script("window.scrollTo(1,document.body.scrollHeight)")  #Scrolls to the bottom of the page 
        ScrollNumber-=1
        sleep(3)
    sleep(4)                                                                    #Sleep for 4 to let the data load
    pagedata=driver.page_source                                                 #gets the htmlsource 
    soup = BeautifulSoup(pagedata,'html.parser')                                   #Parsing the htmldata to get required links 
    for deviantdata in soup.findAll('a',{'data-hook':"deviation_link"}):
        hrefval=deviantdata.get('href')
        alldata.append(hrefval)               
driver.close() 
alldata=list(set(alldata))  

url=["https://www.deviantart.com/tag/steamprofile?order=this-week","https://www.deviantart.com/tag/steamprofiledesigns?order=this-week","https://www.deviantart.com/tag/steamprofile?order=this-month"]
main="https://www.deviantart.com/tag/steamprofiledesign?page="
#generates follow up urls for custom urls 
#recommended to run once 
# for i in range(1,10):
#   url.append(f'https://www.deviantart.com/tag/steamprofiledesign?page={str(i)}')
#Checking for files
if (not os.path.isfile('links.pkl')):
    with open('links.pkl', 'wb') as fp:
        nam=["https://www.deviantart.com/leithon/art/Girl-Pink-Forest-Steam-Profile-Design-882872778","https://www.deviantart.com/mahaka11/art/Zero-Two-Steam-Artwork-Profile-animated-732063179"]
        pickle.dump(nam, fp)
if (not os.path.isfile('data.json')):
    with open('data.json', 'w') as fp:
        fp.write(json.dumps({"https://steamcommunity.com/market/listings/753/379420-Stars": 227.98}))

#pickling to load previous data
with open('links.pkl', "rb") as txtfile:
    onlylinks = pickle.load(txtfile)

with open('data.json') as json_file:  
    data = json.load(json_file)                                               #has the data from prev searches stored in this 
clear()
#get_item(item_name ) should be non url encoded url like
# example get_item("https://steamcommunity.com/market/listings/753/746850-Chinatown" ) returns :₹ 269.36  ( {currency} value )
def get_item(item):
        item=item.replace(url2,"")
        market_hash_name= unquote(item)
        url = f'https://steamcommunity.com/market/priceoverview/?country=US&currency=24&appid={appid}&market_hash_name={market_hash_name}'
        time.sleep(2)
        resp = requests.get(url)
        try:
            jsondata=json.loads(resp.content)
            if resp.ok:      
                print(jsondata+" "+market_hash_name)               
                jsondata=json.loads(resp.content)
                if jsondata['success'] :                                     #if item exits  returns price
                    return jsondata["lowest_price"]
                else:
                    print(item +" has no value") 
            else:
                    print(jsondata+" "+resp.url)
                    print("going to sleep for 5 sec")
                    time.sleep(5)
                    get_item(item)   
        except KeyError:
                return "NA"

#############################################################comment from here#####################################################

#                                                                            #stores page data in the url[]  links only like www.deviantart.com/ artist name /art/ artwork name
for devianturl in url:
    print("Accessing Devient gallery page "+ devianturl)                                     
    main_page = requests.get(devianturl)                                     #accesss the pages
    soup = BeautifulSoup(main_page.content, 'html.parser')                                          
    for deviantdata in soup.findAll('a',{'data-hook':"deviation_link"}):
        hrefval=deviantdata.get('href')
        alldata.append(hrefval)                                                     
alldata=list(set(alldata))                                                    # duplicates removed
#                                                                             #stores all the steam links 

                                                                           
for artworkurls in alldata:
    if (not ( artworkurls in onlylinks)):                                     #visiting each pages to check for steam link brute force*        
        print("Accessing ArtWork page "+ artworkurls)
        onlylinks.append(artworkurls)
        page = requests.get(artworkurls)  
        soup = BeautifulSoup(page.content, 'html.parser')                     #visiting each page and checking for href to steam market 
        for pagedata in soup.findAll('a',{'class':"external"}):
            hrefval=pagedata.get('href')                                      #href val holds all the links which are in the page
            if match_string in hrefval:                                       #match string has the steammarket link
                steamlink.append(hrefval.replace(remove_string,""))           #devient external link is stripped and if matches its added into this set
        

onlylinks=list(set(onlylinks))                                                #sorting and deleting duplicate art work links
steamlink=list(set(steamlink))                                                #sorting and deleting duplicates steamlinks
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
#steamlink=

for i in steamlink:
    try:
        price=get_item(i)
        if(not "NA" in price ):
            price=price.replace('₹','').replace(',','')
            price=float(price)
            if(price >=120.00):                                                 #Appends only if value is greater than 150
                new[i]=price
                data[i]=price
            #data now has merged data from file and new appends to it 
            # Finally writing the data to file
            with open('new.json',"w",encoding='utf-8') as json_file:            #new.json will have newest values be sure to check it after running the program
                json_file.write(json.dumps(new))
    except TypeError: 
        pass
with open('data.json',"w",encoding='utf-8') as json_file:                       # Finally writing the data to file
    json_file.write(json.dumps(data))
with open('links.pkl', "wb") as txtfile:                                        # Pickling the final links to file
    pickle.dump(onlylinks, txtfile)
print("Check /new.json For Latest data")
