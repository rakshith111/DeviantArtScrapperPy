
import pandas as pd
import json
import os
from time import sleep
from libs import urlextractor

import json
import requests
from bs4 import BeautifulSoup
from libs import deviantartapi


class scrapper:
    def __init__(self) -> None:
        '''
        :file: localprice.csv - Contains the steam links and the prices of the items
        :file: failed.csv - Contains the steam links that failed to load due to multiple requests
        :file: deviantXsteam.csv - Contains the links to the deviantart pages and the steam links in the art pages
        :return: None

        | Initializes the class and loads the data from the csv files
        | Initializes the selenium driver and logs in to the account requires a username and password
        | If credentials are not provided, it will request for the credentials
        | Once credentials are provided, it will login to the account and save the cookies



        '''
        self.remove_string = "https://www.deviantart.com/users/outgoing?"
        self.match_string = "https://steamcommunity.com/market/listings/"
        self.data_path = 'src\data'

        # self.data_files=['deviantXsteam.csv','localprice.csv','failed.csv']
        # check if files exists or not and create it
        if (not os.path.isfile(os.path.abspath(os.path.join(self.data_path, 'Credentials.json')))):
            print('[x] Credentials not found, creating new file')
            print('[+] Creating Credentials.json')
            print('[+] Please enter your credentials')
            username = input('Username: ')
            password = input('Password: ')
            with open(os.path.abspath(os.path.join(self.data_path, 'Credentials.json')), 'w') as f:
                json.dump({'username': username, 'password': password}, f)
            print('[+] Logging in with credentials')
            self.deviantartapi = deviantartapi.selenium_scrapper(
                username, password)

        else:
            print('[+] Logging in with credentials')
            with open(os.path.abspath(os.path.join(self.data_path, 'Credentials.json')), 'r') as f:
                credentials = json.load(f)
            self.deviantartapi = deviantartapi.selenium_scrapper(
                credentials['username'], credentials['password'])

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

    def steamlinks_scrapper(self, deviantartpages: list) -> None:
        '''
        :param list deviantartpages:  list of deviant art page links which are to be searched for steam links
        :return: None

        | Accepts a list of deviant art page links
        | Then searches for the steam links in the art pages
        | If steam link is found then it is added to the deviantXsteam.csv file

        '''
        for deviantartpage in deviantartpages:
            print(f"[+] Accessing {deviantartpage}....")
            page = requests.get(deviantartpage)
            soup = BeautifulSoup(page.content, 'html.parser')

            for pagedata in soup.findAll('a', {'class': "external"}):
                hrefval = pagedata.get('href')
                if self.match_string in hrefval:  # match string has the steammarket link
                    hrefval = urlextractor.remove_filter(hrefval)
                    steamlink = (str(hrefval).replace(self.remove_string, ""))
                    #return steamlink

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

    print("ye")
    scrapper()
    dev = deviantartapi.selenium_scrapper()
    k = dev.get_deviant_links(
    ['https://www.deviantart.com/tag/steamprofile?order=this-month'], 4)
    # retrives 96 links in case of no duplicates

    # getsubpages=(scrapper().deviant_scrapper_pages("https://www.deviantart.com/tag/steamprofile",2))
    # print(getsubpages)
    # getsteamliks = scrapper()
    # pp=getsteamliks.steamlinks_scrapper(
    #  ["https://www.deviantart.com/xieon08/art/Shora-Steam-Artwork-Animated-903885045"])
    # print(pp)
    # no steam url https://www.deviantart.com/dryrel/art/CP2077-Rainy-Day-Animated-Steam-Artwork-936861222
