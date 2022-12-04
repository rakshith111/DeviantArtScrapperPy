import json
import time
import re
import requests


from urllib.parse import unquote



def get_item(steamurl: str) -> str:  # type: ignore
    """
    :param str steamurl: Steam url 
    :rtype: str
    :example: get_item("https://steamcommunity.com/market/listings/753/746850-Chinatown" )
    :return: price of the item  returns ₹ 269.36  (price of the item)

    | Takes a steammarket url and returns its price

    """
    patforid = (r"/[\d]+/")
    patforname = (r"/[\d]+-[\w%()-'!$%&*+,-./:;<=>?@[\]^_`{|}~]+")
    appid = re.findall(patforid, steamurl)
    patforname = re.findall(patforname, steamurl)

    url = f'https://steamcommunity.com/market/priceoverview/?country=US&currency=24&appid={appid[0].replace("/","")}&market_hash_name={patforname[0].replace("/","")}'
    time.sleep(2)
    resp = requests.get(url)
    try:
        steamjsondata = json.loads(resp.content)
        if resp.ok:
            steamjsondata = json.loads(resp.content)

            if steamjsondata["lowest_price"]:  # if item exits  returns price
                print(
                    f'Got Price : { steamjsondata["lowest_price"]} Steamurl:{steamurl}  ')
                return steamjsondata["lowest_price"]
            else:
                return "NA"
        else:
            print(resp.url+" going to sleep for 5 sec ")
            print(steamjsondata)
            time.sleep(5)
            get_item(steamurl)
    except KeyError:
        return "NA"
