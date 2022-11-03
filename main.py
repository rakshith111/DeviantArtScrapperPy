
import pandas as pd
import json
import os
import urllib3

import re
import requests
from bs4 import BeautifulSoup
class scrapper:
    def __init__(self) -> None:

        #check if files exists or not and create it
        if (not os.path.isfile('data/deviantXsteam.csv')):
            pd.DataFrame(columns=['Steam_AppId', 'Steam_URL', 'DeviantUrls', 'SteamPrice', 'SteamPriceDate','VisitedCount']).to_csv(
                'data/deviantXsteam.csv', index=False)
        else:
            self.deviantxsteamdf = pd.read_csv('data/deviantXsteam.csv')
            print(self.deviantxsteamdf["Steam_AppId"])

        if (not os.path.isfile('data/failed.csv')):
            pd.DataFrame(columns=['Steam_URL', 'Steam_AppId']).to_csv('data/failed.csv', index=False)
        else:
            self.faileddf = pd.read_csv('data/failed.csv')
    #Re Run failed links
    def deviant_scrapper(self):
        '''
        Visits Main Deviantart page and extracts all the links to the art pages

        
        '''

        current=[]
        # page = requests.get(
        #    "https://www.deviantart.com/tag/steamprofile?order=this-month")
        # page_cookie = page.cookies
        
        # soup = BeautifulSoup(page.content, 'html.parser')
        # with open("temp.html", "w", encoding='utf8') as file:
        #     file.write(page.text)

        with open("2nd.htm", 'r', encoding='utf8') as f:
                    filepage = f.read()
        soup = BeautifulSoup(filepage,features="lxml")
        for deviantdata in soup.findAll('div', {'class': "mWr4e"}):
            hrefval = deviantdata.select(
                'a[data-hook="deviation_link"]')[0]['href']
            current.append(hrefval)



scrapper().deviant_scrapper()
