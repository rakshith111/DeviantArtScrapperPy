import json
import time
import re
import requests


# add proxy support

def get_item(steam_url: str, country_code:int=24) -> str:  # type: ignore
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
        pattern_for_id = ("[\d]+/")
        pattern_for_name = ("[\d]+-[\w%()'!$%&*+,-.:;<=>?@[\]^_`{|}~]+")
        app_id = re.findall(pattern_for_id, steam_url)
        market_hash_name = re.findall(pattern_for_name, steam_url)
    except IndexError:
        print("[-] Error in regex")
        return "RE"

    url = f'https://steamcommunity.com/market/priceoverview/?currency={country_code}&appid={app_id[0].replace("/","")}&market_hash_name={market_hash_name[0].replace("/","")}'
    time.sleep(1)
    print(f'[+] Getting Price for SteamItem: {market_hash_name[0].replace("/","")}')
    resp = requests.get(url)
    steam_json_data = {"NO DATA": "NO DATA"}
    try:
        if resp.ok:
            steam_json_data = json.loads(resp.content)
            if steam_json_data["lowest_price"]:  # if item exits  returns price
                print(
                    f'[+] Got Price for  Steamurl:{steam_url}  {steam_json_data["lowest_price"]}')
                return steam_json_data["lowest_price"]
        else:
            print("[-] Possible timeout, trying again")
            print(resp.url+" going to sleep for 30 sec ")
            print(steam_json_data)
            time.sleep(30)
            return get_item(steam_url)
    except KeyError:
        return "FA"


