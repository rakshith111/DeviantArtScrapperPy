import json
import os
import re
import json
import requests
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup

from libs import urlextractor
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
        self.data_path = r'src\data'

       # self.data_files = ['deviantXsteam.csv', 'localprice.csv', 'failed.csv']
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
            pd.DataFrame(columns=['SteamUrl', 'DeviantUrls']).to_csv(
                os.path.abspath(os.path.join(self.data_path, 'deviantXsteam.csv')), index=False)
        else:
            print('[+] Loading deviantXsteam.csv')
            self.deviantxsteamdf = pd.read_csv(os.path.abspath(
                os.path.join(self.data_path, 'deviantXsteam.csv')))

        if (not os.path.isfile(os.path.abspath(os.path.join(self.data_path, 'localprice.csv')))):
            print('[x] localprice.csv not found, creating new file')
            print('[+] Creating localprice.csv')
            pd.DataFrame(columns=['SteamAppId', 'SteamUrl', 'SteamPrice', 'SteamPriceDate', ]).to_csv(
                os.path.abspath(os.path.join(self.data_path, 'localprice.csv')), index=False)
        else:
            print('[+] Loading localprice.csv')
            self.localpricedf = pd.read_csv(os.path.abspath(
                os.path.join(self.data_path, 'localprice.csv'))
            )

        if (not os.path.isfile(os.path.abspath(os.path.join(self.data_path, 'failed.csv')))):
            print('[x] failed.csv not found, creating new file')
            print('[+] Creating failed.csv')
            pd.DataFrame(columns=['SteamUrl', 'SteamAppId']).to_csv(
                os.path.abspath(os.path.join(self.data_path, 'failed.csv')), index=False)
        else:
            print('[+] Loading failed.csv')
            self.faileddf = pd.read_csv(os.path.abspath(
                os.path.join(self.data_path, 'failed.csv')))
        print('#'*50)

    # Add a rerun function to rerun the failed links

    def steamlinks_scrapper(self, deviantartpages: list,saveafter:int=5) -> None:
        '''
        :param list deviantartpages:  list of deviant art page links which are to be searched for steam links
        :param int saveafter:  number of links to be searched before saving the data 
        :return: None

        | Accepts a list of deviant art page links, then searches for the steam links in the art pages
        | If steam market link is found its added to the deviantXsteam.csv file along with the deviant art page link if not already present 
        | If no steam market link is found, its still added but with a None value for the steam market link
        | Saves data every 5 links to avoid data loss in case of an error
        | `saveafter` Can be overriden 

        '''
        rowdata = []
        datacount = 0
        saveafter = self.saveafter
        for deviantartpage in deviantartpages:
            if deviantartpage in self.deviantxsteamdf['DeviantUrls'].values:
                print('[X] Deviantart page already exists')
                print('[X] Skipping ....')
                continue
            else:
                print(f"[+] Accessing {deviantartpage}....")
                page = requests.get(deviantartpage)
                soup = BeautifulSoup(page.content, 'html.parser')
                outgoingsteam = soup.find('a', {'class': "external"}, href=re.compile(
                    "steamcommunity.com/market/listings"))
                # if steam market link is found
                if outgoingsteam:
                    outgoingsteam = (outgoingsteam.get('href'))
                    outgoingsteam = urlextractor.remove_filter(outgoingsteam)
                    steamlink = (str(outgoingsteam).replace(
                        self.remove_string, ""))
                    print('[+] Steam link found')
                    rowdata.append((steamlink, deviantartpage))
                    datacount += 1
                else:
                    print('[X] No steam link found')
                    rowdata.append((None, deviantartpage))
                    datacount += 1

                # save after 5 links
                if datacount > saveafter:
                    print('[+] Saving data to deviantXsteam.csv')
                    merger = pd.DataFrame(
                        rowdata, columns=['SteamUrl', 'DeviantUrls'])
                    self.deviantxsteamdf = pd.concat(
                        [self.deviantxsteamdf, merger], ignore_index=True)
                    self.deviantxsteamdf.to_csv(os.path.abspath(os.path.join(
                        self.data_path, 'deviantXsteam.csv')), index=False)
                    print('[+] Data saved to deviantXsteam.csv')
                    datacount = 0
                    rowdata = []
        # save remaining data if any
        if len(rowdata) > 0:
            print(f'[+] Saving {len(rowdata)} data to deviantXsteam.csv')
            merger = pd.DataFrame(rowdata, columns=['SteamUrl', 'DeviantUrls'])
            self.deviantxsteamdf = pd.concat(
                [self.deviantxsteamdf, merger], ignore_index=True)
            self.deviantxsteamdf.to_csv(os.path.abspath(os.path.join(
                self.data_path, 'deviantXsteam.csv')), index=False)
            print('[+] Data saved to deviantXsteam.csv')


if __name__ == "__main__":

    # dev = deviantartapi.selenium_scrapper()
    # k = dev.get_deviant_links(
    #     ['parent'], 4)
    # retrives 96 links in case of no duplicates

    getsteamliks = scrapper()
    pp = getsteamliks.steamlinks_scrapper( ["link1","link2"])
