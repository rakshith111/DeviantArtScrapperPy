import time
import os
import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

import urlextractor


class SeleniumScrapper:
    def __init__(self, username=None, password=None) -> None:
        '''
        :param str username: Deviant art username
        :param str password: Deviant art password
        :return: None

        | Initializes the driver,Logs in to the account and loads the page
        | Uses cookies to login to the account if the cookies are present
        | If the cookies are not present, it will login to the account and save the cookies

        '''

        options = Options()
        self.username = username
        self.password = password
        options.headless = True
        options.set_preference("useAutomationExtension", False)
        self.driver = webdriver.Firefox(options=options,)
        self.data_path = r'src\data'
        self.login_url = 'https://www.deviantart.com/users/login'
        self.driver.get(self.login_url)
        print('[+] Headless Firefox Initialized')

        if (not os.path.isfile(os.path.abspath(os.path.join(self.data_path, 'cookie.pkl')))):
            print('[x] Cookie.pkl not found, creating new file')
            self.login()

        else:
            print('[+] Loading Cookies')
            cookies = pickle.load(open(os.path.abspath(
                os.path.join(self.data_path, 'cookie.pkl')), "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.get(self.login_url)
            if self.driver.current_url == self.login_url:
                print('[x] Error in loding cookies, logging in manually')
                self.login()
            print('[+] Cookies loaded')

    def login(self):
        '''
        :return: None

        | Logs in to the account and saves the cookies

        '''

        self.driver.find_element(By.ID, "username").send_keys(self.username)

        self.driver.find_element(
            By.ID, "password").send_keys(self.password)

        self.driver.find_element(By.ID, "loginbutton").click()
        time.sleep(2)
        pickle.dump(self.driver.get_cookies(), open(os.path.abspath(
            os.path.join(self.data_path, 'cookie.pkl')), "wb"))
        print('[+] Cookies saved')

    def get_deviant_links(self, base_url: list, next_page: int = 2) -> set:
        '''
        :param list base_url:  list of Deviant art Base urls
        :param int next_page:  Number of pages to scrape
        :return: set of links to the deviant art pages
        :rtype: set


        .. note::
            Need to enable Paging in Account settings -> Browsing -> Paging -> click through pages

        | Loads the page, Finds all the links to the deviant art pages
        | Then next page cursor is searched and the function is called again with the next page url
        | each page returns 24 links, then 24*next_page links will be returned
        | so if nexpage is 2 then 48 links are returned
        | Next page cursor count can be set manually in the function
        | Returns the set of links

        '''
        self.deviant_art_pages = set()

        for url in base_url:
            next_btn_clicker = 0
            self.driver.get(url)
            print(f"[+] Accessing page {next_btn_clicker+1} = {url} ....")
            time.sleep(5)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

           # with open('deviantart.html', 'w',encoding="utf-8") as f:
            #  f.write(page)
            for a in soup.find_all('a', {'data-hook': "deviation_link"}, href=True):
                self.deviant_art_pages.add(a['href'])
            next_btn_clicker += 1
            find_next_cursor = urlextractor.next_cursor_selenium(
                self.driver.page_source)

            while next_btn_clicker <= next_page-1 and find_next_cursor:
                print(f"[+] Next page cursor = {find_next_cursor}")
                joined_url = "https://www.deviantart.com"+find_next_cursor
                self.driver.get(joined_url)
                print(
                    f"[+] Accessing page {next_btn_clicker+1} = {joined_url}....")
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                for a in soup.find_all('a', {'data-hook': "deviation_link"}, href=True):
                    self.deviant_art_pages.add(a['href'])
                find_next_cursor = urlextractor.next_cursor_selenium(
                    self.driver.page_source)
                next_btn_clicker += 1
                time.sleep(1)
                print(
                    f"[+] Current links found = {len(self.deviant_art_pages)}")
        self.driver.close()
        print(f"[+] Total links found = {len(self.deviant_art_pages)}")
        return self.deviant_art_pages

    def scroll(self, scroll_pause_time: float = 1.5,) -> str:
        '''

        :param int scroll_pause_time:  Time to wait between scrolls
        :return: Page source
        :rtype: str

        .. warning:: 
            **CURRENTLY NOT USED**
            This function returns 24 links per page, even if there are more than 24 links in the page needs to be fixed in the future

        .. note::
            Need to enable scroll Account settings -> Browsing -> Paging -> Scroll through pages

        | Scrolls the page to load all the images
        | Can override the default time to wait between scrolls
        | Gets the scroll height and scrolls to the bottom of the page

        '''

        count = 1
        screen_height = self.driver.execute_script(
            "return window.screen.height;")
        while True:
            print(f'[+] Scrolling {count} times')
            self.driver.execute_script(
                "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=count))
            count += 1
            time.sleep(scroll_pause_time)
            scroll_height = self.driver.execute_script(
                "return document.body.scrollHeight;")
            if (screen_height) * count > scroll_height:
                break
        print("[*] Scrolling done")
        return self.driver.page_source

# if __name__ == "__main__":

#     dev = selenium_scrapper()
#     k = dev.get_deviant_links(
#         ['https://www.deviantart.com/tag/steamprofile?order=this-month'], 4)
