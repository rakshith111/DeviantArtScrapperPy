import json
import time
import re
import requests


# add proxy support

def get_item(steam_url: str, country_code=24) -> str:  # type: ignore
    """
    :param str steam_url: Steam url 
    :param int country_code: country code
    :rtype: str
    :example: get_item("https://steamcommunity.com/market/listings/753/746850-Chinatown" )
    :return: price of the item  returns ₹ 269.36  (price of the item)

    :exception:  IndexError :  RE: Error in regex
    :exception:  NP: No price found
    :exception:  KeyError :  FA: Failed to get price


    | Takes a steammarket url and returns its price
    | Optional country code, default is 24 for Indian-INR, 1 for US-USD

    """
    try:
        patforid = ("[\d]+/")
        patforname = ("[\d]+-[\w%()'!$%&*+,-.:;<=>?@[\]^_`{|}~]+")
        appid = re.findall(patforid, steam_url)
        patforname = re.findall(patforname, steam_url)
    except IndexError:
        print("[-] Error in regex")
        return "RE"
    # print(f'[+] Got Appid for  Steamurl:{steam_url}  {appid[0].replace("/","")}')
    # print(f'[+] Got Name for  Steamurl:{steam_url}  {patforname}')

    url = f'https://steamcommunity.com/market/priceoverview/?currency={country_code}&appid={appid[0].replace("/","")}&market_hash_name={patforname[0].replace("/","")}'
    time.sleep(0.5)
    resp = requests.get(url)
    try:
        if resp.ok:
            steamjsondata = json.loads(resp.content)
            if steamjsondata["lowest_price"]:  # if item exits  returns price
                print(
                    f'[+] Got Price for  Steamurl:{steam_url}  {steamjsondata["lowest_price"]}')
                return steamjsondata["lowest_price"]
            else:
                return "NP"
        else:
            print("[-] Possible timeout, trying again")
            print(resp.url+" going to sleep for 5 sec ")
            print(steamjsondata)
            time.sleep(5)
            get_item(steam_url)
    except KeyError:
        return "FA"
