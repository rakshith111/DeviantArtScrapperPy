
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
        self.remove_string = "https://www.deviantart.com/users/outgoing?"
        self.match_string = "https://steamcommunity.com/market/listings/"
        self.data_path = 'src\data'
        #self.data_files=['deviantXsteam.csv','localprice.csv','failed.csv']
        # check if files exists or not and create it
        if (not os.path.isfile(os.path.abspath(os.path.join(self.data_path, 'deviantXsteam.csv')))):
            print('[x] deviantXsteam.csv not found, creating new file')
            print('[+] Creating deviantXsteam.csv')
            pd.DataFrame(columns=['Steam_AppId', 'Steam_URL', 'DeviantUrls', 'VisitedCount']).to_csv(
                os.path.abspath(os.path.join(self.data_path, 'deviantXsteam.csv')), index=False)
        else:
            print('[+] Loading deviantXsteam.csv')
            self.deviantxsteamdf = pd.read_csv(os.path.abspath(
                os.path.join(self.data_path, 'deviantXsteam.csv')))

        if (not os.path.isfile(os.path.abspath(os.path.join(self.data_path, 'localprice.csv')))):
            print('[x] localprice.csv not found, creating new file')
            print('[+] Creating localprice.csv')
            pd.DataFrame(columns=['Steam_AppId', 'SteamPrice', 'SteamPriceDate', ]).to_csv(
                os.path.abspath(os.path.join(self.data_path, 'localprice.csv')), index=False)
        else:
            print('[+] Loading localprice.csv')
            self.localpricedf = pd.read_csv(os.path.abspath(
                os.path.join(self.data_path, 'localprice.csv'))
            )
        if (not os.path.isfile(os.path.abspath(os.path.join(self.data_path, 'failed.csv')))):
            print('[x] failed.csv not found, creating new file')
            print('[+] Creating failed.csv')
            pd.DataFrame(columns=['Steam_URL', 'Steam_AppId']).to_csv(
                os.path.abspath(os.path.join(self.data_path, 'failed.csv')), index=False)
        else:
            print('[+] Loading failed.csv')
            self.faileddf = pd.read_csv(os.path.abspath(
                os.path.join(self.data_path, 'failed.csv')))
    # Add a rerun function to rerun the failed links

    def deviant_scrapper_pages(self, baseurl: str,nextpage:int=2) -> list:
        '''
        :param baseurl: str - Deviant art page url
        :param nextpage: int - Number of pages to visit
        :return: - list of all the art page links

        | Accepts a deviant url and searches for the sub deviant art links
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
    
    def steamlinks_scrapper(self,deviantartpages:list):
        '''
        :param deviantartpages: list - list of deviant art page links which are to be searched for steam links
        :return: None

        | Accepts a list of deviant art page links
        | Then searches for the steam links in the art pages
        | If steam link is found then it is added to the deviantXsteam.csv file
        
        '''
        for deviantartpage in deviantartpages:
            print(f"Accessing {deviantartpage}....")
            page = requests.get(deviantartpage)
            soup = BeautifulSoup(page.content, 'html.parser')

            for pagedata in soup.findAll('a',{'class':"external"}):
                hrefval=pagedata.get('href')                                    
                if self.match_string in hrefval:                                       #match string has the steammarket link
                    hrefval= urlextractor.remove_filter(hrefval)
                    steamlink=(hrefval.replace(self.remove_string,"")) 
                  
                #     if steamlink:
                #         self.deviantxsteamdf = self.deviantxsteamdf.append(
                #             {'Steam_AppId': steamlink, 'Steam_URL': f"https://store.steampowered.com/app/{steamlink}", 'DeviantUrls': deviantartpage, 'VisitedCount': 1}, ignore_index=True)
                #         self.deviantxsteamdf.to_csv(
                #             'data/deviantXsteam.csv', index=False)
                #     else:
                #         self.faileddf = self.faileddf.append(
                #             {'Steam_URL': f"https://store.steampowered.com/app/{steamlink}", 'Steam_AppId': steamlink}, ignore_index=True)
                #         self.faileddf.to_csv('data/failed.csv', index=False)
                # sleep(2)


if __name__ == "__main__":

   
        # k=(scrapper().deviant_scrapper_pages("https://www.deviantart.com/tag/steamprofile",2))
        k=scrapper()
        k.steamlinks_scrapper(["https://www.deviantart.com/xieon08/art/Shora-Steam-Artwork-Animated-903885045"])
        print((k))
       