
import pandas as pd
import json
import os
from time import sleep
from libs import urlextractor

import requests
from bs4 import BeautifulSoup


class scrapper:
    def __init__(self) -> None:
        '''
        :file: localprice.csv - Contains the steam links and the prices of the items
        :file: failed.csv - Contains the steam links that failed to load due to multiple requests
        :file: deviantXsteam.csv - Contains the links to the deviantart pages and the steam links in the art pages
        :return: None

        | Initializes the class and loads the data from the csv files
    
       
        '''

        # check if files exists or not and create it
        if (not os.path.isfile('data/deviantXsteam.csv')):
            pd.DataFrame(columns=['Steam_AppId', 'Steam_URL', 'DeviantUrls', 'VisitedCount']).to_csv(
                'data/deviantXsteam.csv', index=False)
        else:
            self.deviantxsteamdf = pd.read_csv('data/deviantXsteam.csv')

        if (not os.path.isfile('data/localprice.csv')):
            pd.DataFrame(columns=['Steam_AppId', 'SteamPrice', 'SteamPriceDate', ]).to_csv(
                'data/localprice.csv', index=False)
        else:
            self.localpricedf = pd.read_csv('data/localprice.csv')
        if (not os.path.isfile('data/failed.csv')):
            pd.DataFrame(columns=['Steam_URL', 'Steam_AppId']).to_csv(
                'data/failed.csv', index=False)
        else:
            self.faileddf = pd.read_csv('data/failed.csv')
    # Re Run failed links

    def deviant_scrapper(self, baseurl: str,nextpage:int=2) -> list:
        '''
        :param baseurl: str - Deviant art page url
        :param nextpage: int - Number of pages to visit
        :return: - list of all the art page links

        | Accepts a deviant url and searches for sub deviant art pages
        | Then next page cursor is searched and the function is called again with the next page url
        | each page returns 24 links, then 24*nextpage links will be returned
        | so if nexpage is 2 then 48 links are returned
  
        
        '''

        deviantartpages = []
        NextBtnClicker = 0
        page = requests.get(baseurl)
        page_cookie = page.cookies

        soup = BeautifulSoup(page.content, 'html.parser')
        print(f"Accessing page {NextBtnClicker+1} ={baseurl}....")
        for deviantdata in soup.findAll('div', {'class': "mWr4e"}):
            hrefval = deviantdata.select(
                'a[data-hook="deviation_link"]')[0]['href']
            deviantartpages.append(hrefval)
        # will retrive 24 urls
        NextBtnClicker += 1
        nexts=urlextractor.nextcursor(baseurl,page_cookie)
        while NextBtnClicker <= nextpage-1 and nexts:  

            joinedurl = "https://www.deviantart.com"+nexts
            print(f"Accessing page {NextBtnClicker+1} ={joinedurl}....")
            main_page = requests.get(joinedurl, cookies=page_cookie)
            mp_cookie = main_page.cookies
            soup = BeautifulSoup(main_page.content, 'html.parser')
            for deviantdata in soup.findAll('div', {'class': "mWr4e"}):
                hrefval = deviantdata.select(
                    'a[data-hook="deviation_link"]')[0]['href']
                deviantartpages.append(hrefval)
            nexts = urlextractor.nextcursor(joinedurl, mp_cookie)
            NextBtnClicker += 1
            sleep(2)
        
        return deviantartpages


if __name__ == "__main__":

   
        k=(scrapper().deviant_scrapper("https://www.deviantart.com/tag/steamprofile",2))
     
        print(len(k))
       