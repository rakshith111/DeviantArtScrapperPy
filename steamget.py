import json
import time
from time import sleep
from httpx import stream
import requests
from urllib.parse import unquote
import re

def get_item(steamurl):
        """
        Takes a steamurl and returns its price
        Parameters:
        jsonfile (url): Should be a non url encoded steamurl and non
        example:- get_item("https://steamcommunity.com/market/listings/753/746850-Chinatown" )
    
        Result:
        returns a string
            ( {currency} value )  example:- returns ₹ 269.36  

        """
        patforid=("/[\d]+/")
        patforname=("/[\d]+-[\w]+")
        appid=re.findall(patforid,steamurl)
        patforname=re.findall(patforname,steamurl)
        market_hash_name= unquote(steamurl)
        url = f'https://steamcommunity.com/market/priceoverview/?country=US&currency=24&appid={appid[0].replace("/","")}&market_hash_name={patforname[0].replace("/","")}'
        time.sleep(2)
        resp = requests.get(url)
        try:
            steamjsondata=json.loads(resp.content)
            if resp.ok:
                steamjsondata=json.loads(resp.content)
                
                if steamjsondata["lowest_price"] :                                     #if item exits  returns price
                    print(f'Got Price : { steamjsondata["lowest_price"]} Steamurl:{market_hash_name}  ')
                    return steamjsondata["lowest_price"]
                else:
                    return "NA"
            else:
                    print(steamjsondata+" "+resp.url)
                    print("going to sleep for 5 sec")
                    time.sleep(5)
                    get_item(steamurl)   
        except KeyError:
                return "NA"
                
