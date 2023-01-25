
import os
import re
import datetime
import json
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

from libs import steamapi
from libs import urlextractor
from libs import deviantartapi


class scrapper:
    def __init__(self, dev=False) -> None:
        '''
        :file: localprice.csv - Contains the steam links and the prices of the items
        :file: failed.csv - Contains the steam links that failed to load due to multiple requests
        :file: deviantXsteam.csv - Contains the links to the deviantart pages and the steam links in the art pages
        :param bool dev:  If true, it will skip the login process
        :return: None

        | Initializes the class and loads the data from the csv files
        | Initializes the selenium driver and logs in to the account requires a username and password
        | If credentials are not provided, it will request for the credentials
        | Once credentials are provided, it will login to the account and save the cookies
        | Dev mode is used to skip the login process

        '''
        self.remove_string = "https://www.deviantart.com/users/outgoing?"
        self.match_string = "https://steamcommunity.com/market/listings/"
        self.patfortag = "[\d]+-"
        self.data_path = r'src\data'
        self.today = datetime.datetime.now().strftime(r'%d-%m-%Y')
        self.data_files = ['deviantXsteam.csv', 'localprice.csv', 'failed.csv']

        if dev:
            print("[+] Dev mode enabled, skipping login")
        else:
            self._check_credentials()

        self._check_data_files()

    def _check_credentials(self):
        credentials_path = os.path.abspath(
            os.path.join(self.data_path, 'Credentials.json'))
        if (not os.path.isfile(credentials_path)):
            print('[x] Credentials not found, creating new file')
            print('[+] Creating Credentials.json')
            print('[+] Please enter your credentials')
            username = input('Username: ')
            password = input('Password: ')
            with open(credentials_path, 'w') as f:
                json.dump({'username': username, 'password': password}, f)
            print('[+] Starting login process...')
            self.deviantartapi = deviantartapi.selenium_scrapper(
                username, password)
        else:
            print('[+] Logging in with credentials')
            with open(credentials_path, 'r') as f:
                credentials = json.load(f)
            self.deviantartapi = deviantartapi.selenium_scrapper(
                credentials['username'], credentials['password'])

    def _check_data_files(self):
        for file in self.data_files:
            file_path = os.path.abspath(os.path.join(self.data_path, file))
            if (not os.path.isfile(file_path)):
                print(f'[x] {file} not found, creating new file')
                print(f'[+] Creating {file}')
                if file == 'deviantXsteam.csv':
                    pd.DataFrame(columns=['SteamUrl', 'DeviantUrl','visited?']).to_csv(
                        file_path, index=False)
                    self.deviantxsteamdf = pd.read_csv(file_path)
                elif file == 'localprice.csv':
                    pd.DataFrame(columns=['AppTag', 'SteamUrl', 'SteamPrice', 'SteamPriceDate']).to_csv(
                        file_path, index=False)
                    self.localpricedf = pd.read_csv(file_path)
                elif file == 'failed.csv':
                    pd.DataFrame(columns=['AppTag', 'SteamUrl', 'Date']).to_csv(
                        file_path, index=False)
                    self.faileddf = pd.read_csv(file_path)
            else:
                print(f'[+] Loading {file}')
                if file == 'deviantXsteam.csv':
                    self.deviantxsteamdf = pd.read_csv(file_path)
                elif file == 'localprice.csv':
                    self.localpricedf = pd.read_csv(file_path)
                elif file == 'failed.csv':
                    self.faileddf = pd.read_csv(file_path)
        print('#'*50+' Done loading '+'#'*50)

    def file_reload(self) -> None:
        '''
        | Reloads the data from the csv files
        | This is used when the data is updated in the csv files

        :return: None
        '''
        print("[+] Re-loading data files")
        for file in self.data_files:
            file_path = os.path.abspath(os.path.join(self.data_path, file))
            if file == 'deviantXsteam.csv':
                self.deviantxsteamdf = pd.read_csv(file_path)
            elif file == 'localprice.csv':
                self.localpricedf = pd.read_csv(file_path)
            elif file == 'failed.csv':
                self.faileddf = pd.read_csv(file_path)

    # Add a rerun function to rerun the failed links

    def steamlinks_scrapper(self, deviantartpages: list, saveafter: int = 5) -> None:
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
        self.saveafter = saveafter
        difflinks = set(deviantartpages) - \
            set(self.deviantxsteamdf['DeviantUrl'])
        for deviantartpage in difflinks:
            print(f"[+] Accessing {deviantartpage}....")
            time.sleep(2)
            page = requests.get(deviantartpage)
            soup = BeautifulSoup(page.content, 'html.parser')
            outgoingsteam = soup.find('a', {'class': "external"}, href=re.compile(
                "steamcommunity.com/market/listings"))

            if outgoingsteam:
                outgoingsteam = (outgoingsteam.get('href'))  # type: ignore
                outgoingsteam = urlextractor.remove_filter(str(outgoingsteam))
                steamlink = (str(outgoingsteam).replace(
                    self.remove_string, ""))
                print('[+] Steam link found')
                rowdata.append((steamlink, deviantartpage, "yes"))
                datacount += 1
            else:
                print('[x] No steam link found')
                rowdata.append((None, deviantartpage, "yes-nolink"))
                datacount += 1

            if datacount > self.saveafter:
                print('[+] Saving data to deviantXsteam.csv')
                new_data = pd.DataFrame(
                    rowdata, columns=['SteamUrl', 'DeviantUrl','visited?'])
                self.deviantxsteamdf = pd.concat(
                    [self.deviantxsteamdf, new_data], ignore_index=True)
                self.deviantxsteamdf.to_csv(os.path.abspath(os.path.join(
                    self.data_path, 'deviantXsteam.csv')), index=False)
                print('[+] Data saved to deviantXsteam.csv')
                datacount = 0
                rowdata = []

        if len(rowdata) > 0:
            print(f'[+] Saving {len(rowdata)} data to deviantXsteam.csv')
            new_data = pd.DataFrame(rowdata, columns=['SteamUrl', 'DeviantUrl','visited?'])
            self.deviantxsteamdf = pd.concat(
                [self.deviantxsteamdf, new_data], ignore_index=True)
            #self.deviantartapi.drop_duplicates( inplace=True)
            self.deviantxsteamdf.to_csv(os.path.abspath(os.path.join(
                self.data_path, 'deviantXsteam.csv')), index=False)
            print('[+] Data saved to deviantXsteam.csv')

    def price_finder(self, saveafter: int = 5) -> None:

        # add a way to accept failed and deviantXsteam links
        # load via diff methods
        '''
        :param int saveafter:  number of links to be searched before saving the data
        :return: None

        | Accepts a list of deviant art page links, then searches for the steam links in the art pages
        | If steam market link is found its added to the deviantXsteam.csv file along with the deviant art page link if not already present
        | If no steam market link is found, its still added but with a None value for the steam market link
        | Saves data every 5 links to avoid data loss in case of an error
        | `saveafter` Can be overriden

        '''
        self.file_reload()
        rowdata = []
        datacount = 0
        self.saveafter = saveafter
        self.steam_urls = self.deviantxsteamdf["SteamUrl"].dropna()
        difflinks = set(self.steam_urls) - \
            set(self.localpricedf['SteamUrl'])
        for steamlink in difflinks:
            price = steamapi.get_item(steamlink)
            if len(price) >= 3:
                price = price.replace("₹ ", "")
                app_tag = re.findall(self.patfortag, steamlink)[
                    0].replace("-", "")
                rowdata.append((app_tag, steamlink, price, self.today))
                datacount += 1
            else:
                price = 0
                rowdata.append((app_tag, steamlink, price, self.today))
                datacount += 1

            if datacount > self.saveafter:
                print('[+] Saving data to localprice.csv')
                merger = pd.DataFrame(
                    rowdata, columns=['AppTag', 'SteamUrl', 'SteamPrice', 'SteamPriceDate'])
                self.localpricedf = pd.concat(
                    [self.localpricedf, merger], ignore_index=True)
                self.localpricedf.to_csv(os.path.abspath(os.path.join(
                    self.data_path, 'localprice.csv')), index=False)
                print('[+] Data saved to localprice.csv')
                datacount = 0
                rowdata = []
        # save remaining data if any
        if len(rowdata) > 0:
            print(f'[+] Saving {len(rowdata)} data to localprice.csv')
            merger = pd.DataFrame(
                rowdata, columns=['AppTag', 'SteamUrl', 'SteamPrice', 'SteamPriceDate'])
            self.localpricedf = pd.concat(
                [self.localpricedf, merger], ignore_index=True)
            self.localpricedf.to_csv(os.path.abspath(os.path.join(
                self.data_path, 'localprice.csv')), index=False)
            print('[+] Data saved to localprice.csv')


if __name__ == '__main__':

    mainscrapper = scrapper(dev=False)
    links = open(os.path.abspath("src\data\links.txt"), "r").readlines()
    artlinks = mainscrapper.deviantartapi.get_deviant_links(links, 3)
    mainscrapper.steamlinks_scrapper(list(artlinks))
    mainscrapper.price_finder()
    from streamlit.web import cli as stcli
    from streamlit import runtime
    import sys
    if not runtime.exists():
        sys.argv = ["streamlit", "run",
                    os.path.abspath("src\libs\htmlgeny.py")]
        sys.exit(stcli.main())
