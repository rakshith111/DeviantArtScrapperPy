
import os
import re
import datetime
import json
import time
import sys
import requests
import pandas as pd
from bs4 import BeautifulSoup
from streamlit.web import cli as stcli
from streamlit import runtime


from libs import steamapi
from libs import urlextractor
from libs import deviantartapi


class DeviantArtScrapper:
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
        self.pattern_for_app_id = "[\d]+-"
        self.data_path = r'src\data'
        self.date_today = datetime.datetime.now().strftime(r'%d-%m-%Y')
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
            with open(credentials_path, 'w') as file:
                json.dump({'username': username, 'password': password}, file)
            print('[+] Starting login process...')
            self.deviant_art_api = deviantartapi.SeleniumScrapper(
                username, password)
        else:
            print('[+] Logging in with credentials')
            with open(credentials_path, 'r') as file:
                credentials = json.load(file)
            self.deviant_art_api = deviantartapi.SeleniumScrapper(
                credentials['username'], credentials['password'])

    def _check_data_files(self):
        for file in self.data_files:
            file_path = os.path.abspath(os.path.join(self.data_path, file))
            if (not os.path.isfile(file_path)):
                print(f'[x] {file} not found, creating new file')
                print(f'[+] Creating {file}')
                if file == 'deviantXsteam.csv':
                    pd.DataFrame(columns=['SteamUrl', 'DeviantUrl', 'visited?']).to_csv(
                        file_path, index=False)
                    self.deviant_x_steam_df = pd.read_csv(file_path)
                elif file == 'localprice.csv':
                    pd.DataFrame(columns=['AppTag', 'SteamUrl', 'SteamPrice', 'SteamPriceDate']).to_csv(
                        file_path, index=False)
                    self.local_price_df = pd.read_csv(file_path)
                elif file == 'failed.csv':
                    pd.DataFrame(columns=['AppTag', 'SteamUrl', 'Date']).to_csv(
                        file_path, index=False)
                    self.failed_df = pd.read_csv(file_path)
            else:
                print(f'[+] Loading {file}')
                if file == 'deviantXsteam.csv':
                    self.deviant_x_steam_df = pd.read_csv(file_path)
                elif file == 'localprice.csv':
                    self.local_price_df = pd.read_csv(file_path)
                elif file == 'failed.csv':
                    self.failed_df = pd.read_csv(file_path)
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
                self.deviant_x_steam_df = pd.read_csv(file_path)
            elif file == 'localprice.csv':
                self.local_price_df = pd.read_csv(file_path)
            elif file == 'failed.csv':
                self.failed_df = pd.read_csv(file_path)

    # Add a rerun function to rerun the failed links

    def steam_links_scrapper(self, deviant_art_pages: list, save_after: int = 5) -> None:
        '''
        :param list deviant_art_pages:  list of deviant art page links which are to be searched for steam links
        :param int save_after:  number of links to be searched before saving the data default is 5
        :return: None

        | Accepts a list of deviant art page links, then searches for the steam links in the art pages
        | If steam market link is found its added to the deviantXsteam.csv file along with the deviant art page link if not already present
        | If no steam market link is found, its still added but with a None value for the steam market link
        | Saves data every 5 links to avoid data loss in case of an error
        | `saveafter` Can be overriden

        '''
        row_data = []
        data_count = 0
        self.save_after = save_after
        difference_links = set(deviant_art_pages) - \
            set(self.deviant_x_steam_df['DeviantUrl'])
        print(f"[+] Total links found = {len(deviant_art_pages)}")
        print(
            f"[+] Removing already searched links = {len(deviant_art_pages) - len(difference_links)}")
        print(f"[+] Total links to be searched: {len(difference_links)}")
        for deviantartpage in difference_links:
            print(f"[+] Accessing {deviantartpage}....")
            time.sleep(2)
            page = requests.get(deviantartpage)
            soup = BeautifulSoup(page.content, 'html.parser')
            outgoing_steam_link = soup.find('a', {'class': "external"}, href=re.compile(
                "steamcommunity.com/market/listings"))

            if outgoing_steam_link:
                outgoing_steam_link = (
                    outgoing_steam_link.get('href'))  # type: ignore
                outgoing_steam_link = urlextractor.url_cleaner(
                    str(outgoing_steam_link))
                steam_link = (str(outgoing_steam_link).replace(
                    self.remove_string, ""))
                print('[+] Steam link found')
                row_data.append((steam_link, deviantartpage, "yes"))
                data_count += 1
            else:
                print('[x] No steam link found')
                row_data.append((None, deviantartpage, "yes-nolink"))
                data_count += 1

            if data_count > self.save_after:
                print('[+] Saving data to deviantXsteam.csv')
                new_data = pd.DataFrame(
                    row_data, columns=['SteamUrl', 'DeviantUrl', 'visited?'])
                self.deviant_x_steam_df = pd.concat(
                    [self.deviant_x_steam_df, new_data], ignore_index=True)
                self.deviant_x_steam_df.to_csv(os.path.abspath(os.path.join(
                    self.data_path, 'deviantXsteam.csv')), index=False)
                print('[+] Data saved to deviantXsteam.csv')
                data_count = 0
                row_data = []

        if len(row_data) > 0:
            print(f'[+] Saving {len(row_data)} data to deviantXsteam.csv')
            new_data = pd.DataFrame(
                row_data, columns=['SteamUrl', 'DeviantUrl', 'visited?'])
            self.deviant_x_steam_df = pd.concat(
                [self.deviant_x_steam_df, new_data], ignore_index=True)
            # self.deviantartapi.drop_duplicates( inplace=True)
            self.deviant_x_steam_df.to_csv(os.path.abspath(os.path.join(
                self.data_path, 'deviantXsteam.csv')), index=False)
            print('[+] Data saved to deviantXsteam.csv')

    def price_finder(self, save_after: int = 5) -> None:

        # add a way to accept failed and deviantXsteam links
        # load via diff methods
        '''
        :param int save_after:  number of links to be searched before saving the data
        :return: None

        | Accepts a list of deviant art page links, then searches for the steam links in the art pages
        | If steam market link is found its added to the deviantXsteam.csv file along with the deviant art page link if not already present
        | If no steam market link is found, its still added but with a None value for the steam market link
        | Saves data every 5 links to avoid data loss in case of an error
        | `save_after` Can be overriden

        '''
        self.file_reload()
        row_data = []
        data_count = 0
        self.save_after = save_after
        self.steam_urls = self.deviant_x_steam_df["SteamUrl"].dropna()
        difference_links = set(self.steam_urls) - \
            set(self.local_price_df['SteamUrl'])
        print(f"[+] Total links found = {len(self.steam_urls)}")
        print(
            f"[+] Removing already searched links = {len(self.steam_urls) - len(difference_links)}")
        print(f"[+] Total links to be searched: {len(difference_links)}")
        for steam_link in difference_links:
            price = steamapi.get_item(steam_link)
            if len(price) >= 3:
                price = price.replace("₹ ", "")
                app_tag = re.findall(self.pattern_for_app_id, steam_link)[
                    0].replace("-", "")
                row_data.append((app_tag, steam_link, price, self.date_today))
                data_count += 1
            else:
                price = 0
                row_data.append((app_tag, steam_link, price, self.date_today))
                data_count += 1

            if data_count > self.save_after:
                print('[+] Saving data to localprice.csv')
                merger = pd.DataFrame(
                    row_data, columns=['AppTag', 'SteamUrl', 'SteamPrice', 'SteamPriceDate'])
                self.local_price_df = pd.concat(
                    [self.local_price_df, merger], ignore_index=True)
                self.local_price_df.to_csv(os.path.abspath(os.path.join(
                    self.data_path, 'localprice.csv')), index=False)
                print('[+] Data saved to localprice.csv')
                data_count = 0
                row_data = []
        # save remaining data if any
        if len(row_data) > 0:
            print(f'[+] Saving {len(row_data)} data to localprice.csv')
            merger = pd.DataFrame(
                row_data, columns=['AppTag', 'SteamUrl', 'SteamPrice', 'SteamPriceDate'])
            self.local_price_df = pd.concat(
                [self.local_price_df, merger], ignore_index=True)
            self.local_price_df.to_csv(os.path.abspath(os.path.join(
                self.data_path, 'localprice.csv')), index=False)
            print('[+] Data saved to localprice.csv')


if __name__ == '__main__':

    scrapper = DeviantArtScrapper(dev=False)
    links = open(os.path.abspath("src\data\links.txt"), "r").readlines()
    links_to_scrape = 14
    pages_to_check = 4
    art_links = scrapper.deviant_art_api.get_deviant_links(
        links[0:links_to_scrape], pages_to_check)
    scrapper.steam_links_scrapper(list(art_links))
    scrapper.price_finder()
    if not runtime.exists():
        sys.argv = ["streamlit", "run",
                    os.path.abspath("src\libs\htmlgeny.py")]
        sys.exit(stcli.main())
