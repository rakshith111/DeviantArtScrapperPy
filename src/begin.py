import json
import os
import pickle
import re
import requests

from bs4 import BeautifulSoup
from libs.htmgeny import htmlgen
from libs.urlextractor import *
from libs.steamget import get_item


class scrapper:
    devianturls = set()
    availablelinks = set()
    availcount = 10
    currcount = 0
    visited = set()
    data = dict()
    latest = dict()
    steamlinks = set()
    failedlinks = []
    urls = []
    data_keys = []
    match_string = "https://steamcommunity.com/market/listings/"
    remove_string = "https://www.deviantart.com/users/outgoing?"

    def __init__(self) -> None:
        '''
        .. warning:: 
            Deprecated - need to update Only kept as a reference

        (visited)    links.pkl:consists of previously visited deviantart page links so that they arent visited more than once
        (failedlinks)failed.pkl:contains steam links which failed to get steam price due to naming or unknown error 
        (data)       data.json: contains all visited steam links with prices , if the steam link appears again in another art page its price will be updated
        (url)        links.txt: list of all the links to check with

        '''
        # check if files exists or not and create it
        if (not os.path.isfile('links.pkl')):
            with open('links.pkl', 'wb') as pf:
                init = ["Blank", "Blank1"]
                pickle.dump(init, pf)
        if (not os.path.isfile('failed.pkl')):
            with open('failed.pkl', 'wb') as pf:
                init = ["https://steamcommunity.com/market/listings/753/447850-Void",
                        "https://steamcommunity.com/market/listings/753/554660-Puzzle%20Poker%20Card"]
                pickle.dump(init, pf)
        if (not os.path.isfile('data.json')):
            with open('data.json', 'w') as jf:
                jf.write(json.dumps({"LINKS": "values"}))
        if (not os.path.isfile('lastavaailable.txt')):
            with open('lastavaailable.txt', 'w') as jf:
                jf.write("")
        # if files exist retrieve data
        with open('links.pkl', "rb") as file:
            self.visited = set(pickle.load(file))
        try:
            with open('failed.pkl', "rb") as file:
                self.failedlinks = pickle.load(file)
        except EOFError:
            self.failedlinks = list()
        with open('data.json') as json_file:
            self.data = json.load(json_file)
            self.data_keys = self.data.keys()
        with open("links.txt", 'r') as file:
            self.urls = json.loads(file.read())

    def writer(self):
        '''
        Writes the data to json file
        '''
        with open('latest.json', "w", encoding='utf-8') as json_file:
            json_file.write(json.dumps(self.latest))
        with open('data.json', "w", encoding='utf-8') as json_file:
            json_file.write(json.dumps(self.data))
        with open('failed.pkl', "wb") as txtfile:
            pickle.dump(self.failedlinks, txtfile)
        with open('links.pkl', "wb") as txtfile:
            pickle.dump(list(self.visited), txtfile)

    def rerunner(self):
        '''
        Reruns the scrapper for the failed links
        '''
        if(len(self.failedlinks) > 0):
            print("\n Re-Running missed items\n\n")
            for link in self.failedlinks:
                link = remove_filter(link)
                try:
                    price = get_item(link)
                    if(not "NA" in price):
                        price = float(re.findall("[\d,]+[\.][\d]+", price)[0])
                        if(price >= 100.00):  # Appends only if value is greater than 100
                            self.latest[link] = price
                            self.data[link] = price
                            self.failedlinks.remove(link)
                except TypeError:
                    self.failedlinks.append(link)
                    print(link+" failed ")
                    pass
        with open('data.json', "w", encoding='utf-8') as json_file:
            json_file.write(json.dumps(self.data))
        self.failedlinks = list(set(self.failedlinks))
        # Pickling the final links to file
        with open('failed.pkl', "wb") as file:
            pickle.dump(self.failedlinks, file)
        htmlgen("data.json")
        htmlgen("latest.json")
        print("Check latest.html For Latest data")
        print("Done")

    def D_link_extractor(self):
        '''
        Extracts the deviant art links from the deviantart page
        '''

        for devianturl in self.urls:
            print("Accessing Deviant gallery page " + devianturl)
            NextBtnClicker = 1
            page = requests.get(devianturl)
            page_cookie = page.cookies
            soup = BeautifulSoup(page.content, 'html.parser')
            for deviantdata in soup.findAll('a', {'data-hook': "deviation_link"}):
                hrefval = deviantdata.get('href')
                self.devianturls.add(hrefval)
        nexts = nextcursor_requests(devianturl, page_cookie)
        while NextBtnClicker <= 1 and nexts:  # Change 2 to any number less than 5 after inital run
            print(f"Accessing page {NextBtnClicker}....")
            joinedurl = devianturl+"&"+nexts
            main_page = requests.get(joinedurl, cookies=page_cookie)
            mp_cookie = main_page.cookies
            soup = BeautifulSoup(main_page.content, 'html.parser')
            for deviantdata in soup.findAll('a', {'data-hook': "deviation_link"}):
                hrefval = deviantdata.get('href')
                self.devianturls.add(hrefval)
            nexts = nextcursor_requests(joinedurl, mp_cookie)
            NextBtnClicker += 1
            sleep(2)
        self.availablelinks = self.devianturls-self.visited
        print(
            f"Links extracted ={len(self.devianturls)} \nAccessing {len(self.availablelinks)} links...")
        with open("lastavaailable.txt", "w") as f:
            json.dump(list(self.availablelinks), f)

    def S_link_extractor(self):
        '''
        Extracts the steam lins links from the art pages
        '''

        for index, artworkurls in enumerate(self.availablelinks):
            print(f"Accessing ArtWork page {index}")
            self.visited.add(artworkurls)
            page = requests.get(artworkurls)
            soup = BeautifulSoup(page.content, 'html.parser')
            for pagedata in soup.findAll('a', {'class': "external"}):
                hrefval = pagedata.get('href')
                if self.match_string in hrefval:  # match string has the steammarket link
                    hrefval = remove_filter(hrefval)
                    # deviant external link is stripped and if matches its added into this set
                    self.steamlinks.add(
                        hrefval.replace(self.remove_string, ""))
        print(f"{len(self.steamlinks)} steam links extracted")
        self.availcount = len(self.steamlinks)
        self.availablelinks = set()
        with open("lastavaailable.txt", "w") as f:
            json.dump(list(self.availablelinks), f)
        with open("laststeam.txt", "w") as f:
            json.dump(list(self.steamlinks), f)
        print("Current Steam links saved to file : laststeam.txt \nRun it with another prog if the script breaks ")

    def pricefetch(self):
        '''
        Fetches the price of the steam links
        '''
        while(self.currcount < self.availcount):
            for link in self.steamlinks:
                try:
                    price = get_item(link)
                    self.currcount += 1
                    if(not "NA" in price):
                        price = float(re.findall("[\d]+.[\d]+", price)[0])
                        if(price >= 100.00):  # Appends only if value is greater than 100
                            self.latest[link] = price
                            self.data[link] = price
                except TypeError:
                    self.failedlinks.append(link)
                    print(link+" failed ")
                    pass
            self.steamlinks = set()
            with open("laststeam.txt", "w") as f:
                json.dump(list(self.steamlinks), f)
# if __name__=="__main__":

#     scapper = scrapper()
#     visited = scapper.visited
#     failedlinks = scapper.failedlinks
#     match_string = scapper.match_string
#     remove_string = scapper.remove_string
#     url = scapper.urls
#     data = scapper.data
#     data_keys = scapper.data_keys
#     latest = scapper.latest
#     availablelinks = scapper.availablelinks
#     steamlinks = scapper.steamlinks
#     if (os.path.getsize("lastavaailable.txt")) > 2:
#         with open("lastavaailable.txt", "r") as f:
#             availablelinks = set(json.loads(f.read()))
#     else:
#         scapper.D_link_extractor()
#     if (os.path.getsize("laststeam.txt")) > 2:
#         with open("laststeam.txt", "r") as f:
#             steamlinks = set(json.loads(f.read()))
#     else:
#         scapper.S_link_extractor()

#     scapper.pricefetch()
#     scapper.rerunner()


#     scapper.writer()
