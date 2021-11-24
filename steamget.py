import json
import time
from time import sleep
import requests
from urllib.parse import unquote
url2="https://steamcommunity.com/market/listings/753/"
appid=int(753)  
def get_item(item):
        """
        Takes a steamurl and returns its price
        example  returns :
        Parameters:
        jsonfile (url): Should be a non url encoded steamurl and non
        example:- get_item("https://steamcommunity.com/market/listings/753/746850-Chinatown" )
    
        Result:
        returns a string
            ( {currency} value )  example:- returns ₹ 269.36  
        """
        print(item)
        item=item.replace(url2,"")
        market_hash_name= unquote(item)
        url = f'https://steamcommunity.com/market/priceoverview/?country=US&currency=24&appid={appid}&market_hash_name={market_hash_name}'
        time.sleep(2)
        resp = requests.get(url)
        try:
            steamjsondata=json.loads(resp.content)
            if resp.ok:   
                print(steamjsondata)        
                print(market_hash_name)   
                steamjsondata=json.loads(resp.content)
                if steamjsondata["lowest_price"] :                                     #if item exits  returns price
                    return steamjsondata["lowest_price"]
                else:
                    return "NA"
            else:
                    print(steamjsondata+" "+resp.url)
                    print("going to sleep for 5 sec")
                    time.sleep(5)
                    get_item(item)   
        except KeyError:
                return "NA"
                
