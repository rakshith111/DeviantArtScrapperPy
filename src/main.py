import json
import os
import re
import json
import requests
import pandas as pd
import datetime

from bs4 import BeautifulSoup

from libs import steamget, urlextractor
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



        '''
        self.remove_string = "https://www.deviantart.com/users/outgoing?"
        self.match_string = "https://steamcommunity.com/market/listings/"
        self.patfortag = ("[\d]+-")
        self.data_path = r'src\data'
        self.today = datetime.datetime.now().strftime(r'%d-%m-%Y')

        #self.data_files = ['deviantXsteam.csv', 'localprice.csv', 'failed.csv']

        if dev:
            print("[+] Dev mode enabled, skipping login")
        else:
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
        # check if files exists or not and create it
        if (not os.path.isfile(os.path.abspath(os.path.join(self.data_path, 'deviantXsteam.csv')))):
            print('[x] deviantXsteam.csv not found, creating new file')
            print('[+] Creating deviantXsteam.csv')
            pd.DataFrame(columns=['SteamUrl', 'DeviantUrls']).to_csv(
                os.path.abspath(os.path.join(self.data_path, 'deviantXsteam.csv')), index=False)
            self.deviantxsteamdf = pd.read_csv(os.path.abspath(
                os.path.join(self.data_path, 'deviantXsteam.csv')))
        else:
            print('[+] Loading deviantXsteam.csv')
            self.deviantxsteamdf = pd.read_csv(os.path.abspath(
                os.path.join(self.data_path, 'deviantXsteam.csv')))

        if (not os.path.isfile(os.path.abspath(os.path.join(self.data_path, 'localprice.csv')))):
            print('[x] localprice.csv not found, creating new file')
            print('[+] Creating localprice.csv')
            pd.DataFrame(columns=['App_Tag', 'SteamUrl', 'SteamPrice', 'SteamPriceDate', ]).to_csv(
                os.path.abspath(os.path.join(self.data_path, 'localprice.csv')), index=False)
            self.localpricedf = pd.read_csv(os.path.abspath(
                os.path.join(self.data_path, 'localprice.csv'))
            )
        else:
            print('[+] Loading localprice.csv')
            self.localpricedf = pd.read_csv(os.path.abspath(
                os.path.join(self.data_path, 'localprice.csv'))
            )

        if (not os.path.isfile(os.path.abspath(os.path.join(self.data_path, 'failed.csv')))):
            print('[x] failed.csv not found, creating new file')
            print('[+] Creating failed.csv')
            pd.DataFrame(columns=['SteamUrl', 'App_Tag']).to_csv(
                os.path.abspath(os.path.join(self.data_path, 'failed.csv')), index=False)
            self.faileddf = pd.read_csv(os.path.abspath(
                os.path.join(self.data_path, 'failed.csv')))
        else:
            print('[+] Loading failed.csv')
            self.faileddf = pd.read_csv(os.path.abspath(
                os.path.join(self.data_path, 'failed.csv')))
        print('#'*50+' Done loading '+'#'*50)

    def file_reload(self) -> None:
        '''
        | Reloads the data from the csv files
        | This is used when the data is updated in the csv files

        :return: None
        '''
        print('[+] Re-Loading failed.csv')
        self.faileddf = pd.read_csv(os.path.abspath(
            os.path.join(self.data_path, 'failed.csv')))
        print('[+] Re-Loading localprice.csv')
        self.localpricedf = pd.read_csv(os.path.abspath(
            os.path.join(self.data_path, 'localprice.csv')))
        print('[+] Re-Loading deviantXsteam.csv')
        self.deviantxsteamdf = pd.read_csv(os.path.abspath(
            os.path.join(self.data_path, 'deviantXsteam.csv')))

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
            set(self.deviantxsteamdf['DeviantUrls'])
        for deviantartpage in difflinks:
            print(f"[+] Accessing {deviantartpage}....")
            page = requests.get(deviantartpage)
            soup = BeautifulSoup(page.content, 'html.parser')
            outgoingsteam = soup.find('a', {'class': "external"}, href=re.compile(
                "steamcommunity.com/market/listings"))
            # if steam market link is found
            if outgoingsteam:
                outgoingsteam = (outgoingsteam.get('href'))  # type: ignore
                outgoingsteam = urlextractor.remove_filter(str(outgoingsteam))
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
            if datacount > self.saveafter:
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
       # self.file_reload()
        rowdata = []
        datacount = 0
        self.saveafter = saveafter
        self.steam_urls = self.deviantxsteamdf["SteamUrl"].dropna()
        difflinks = set(self.steam_urls) - \
            set(self.localpricedf['SteamUrl'])
        for steamlinks in difflinks:
            price = steamget.get_item(steamlinks).replace("₹ ", "")
            app_tag = re.findall(self.patfortag, steamlinks)[
                0].replace("-", "")
            rowdata.append((app_tag,steamlinks, price, self.today))
            datacount += 1

            if datacount > self.saveafter:
                print('[+] Saving data to localprice.csv')
                merger = pd.DataFrame(
                    rowdata, columns=['App_Tag', 'SteamUrl', 'SteamPrice', 'SteamPriceDate'])
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
                rowdata, columns=['App_Tag', 'SteamUrl', 'SteamPrice', 'SteamPriceDate'])
            self.localpricedf = pd.concat(
                [self.localpricedf, merger], ignore_index=True)
            self.localpricedf.to_csv(os.path.abspath(os.path.join(
                self.data_path, 'localprice.csv')), index=False)
            print('[+] Data saved to localprice.csv')


if __name__ == "__main__":

    # dev = deviantartapi.selenium_scrapper()
    # k = dev.get_deviant_links(
    #     ['parent'], 4)
    # retrives 96 links in case of no duplicates

    getsteamliks = scrapper(True)

    gg = getsteamliks.price_finder()
