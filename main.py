
import pandas as pd
import json
import os
import urllib3

import re
import requests
from bs4 import BeautifulSoup


class scrapper:
    def __init__(self) -> None:
        '''
        Initializes the class and loads the data from the csv files
        failed.csv - contains the steam links that failed to load due to multiple requests

        '''

        # check if files exists or not and create it
        if (not os.path.isfile('data/deviantXsteam.csv')):
            pd.DataFrame(columns=['Steam_AppId', 'Steam_URL', 'DeviantUrls', 'VisitedCount']).to_csv(
                'data/deviantXsteam.csv', index=False)
        else:
            self.deviantxsteamdf = pd.read_csv('data/deviantXsteam.csv')

        if (not os.path.isfile('data/localprice.csv')):
            pd.DataFrame(columns=['SteamPrice', 'SteamPriceDate', ]).to_csv(
                'data/localprice.csv', index=False)
        else:
            self.localpricedf = pd.read_csv('data/localprice.csv')
        if (not os.path.isfile('data/failed.csv')):
            pd.DataFrame(columns=['Steam_URL', 'Steam_AppId']).to_csv(
                'data/failed.csv', index=False)
        else:
            self.faileddf = pd.read_csv('data/failed.csv')
    # Re Run failed links

    def deviant_scrapper(self, baseurl: str):
        '''
        Visits Main Deviantart page and extracts all the links to the art pages
        baseurl : str - Deviantart page url


        '''

        current = []
        page = requests.get(baseurl)
        page_cookie = page.cookies

        soup = BeautifulSoup(page.content, 'html.parser')
        with open("temp.html", "w", encoding='utf8') as file:
            file.write(page.text)

        for deviantdata in soup.findAll('div', {'class': "mWr4e"}):
            hrefval = deviantdata.select(
                'a[data-hook="deviation_link"]')[0]['href']
            current.append(hrefval)


if __name__ == "__main__":

    scrapper().deviant_scrapper()
