import json
import os
import requests

from bs4 import BeautifulSoup
from time import sleep
from libs import urlextractor
from json2html import json2html


def htmlgen(jsonfile) -> None:
    """
    :param str jsonfile: json file name(path)

    :return: None

    .. role:: raw-html(raw)
       :format: html

    .. deprecated:: 0.0.1
       :raw-html:`<br />`
       **Only kept as a reference as pandas will use different methods**


    | Generates and opens a html file for the given jsonfile 
    | A html page is generated and opened.
    | Note: A defualt brower must be set by windows 



    """
    if (os.path.getsize(jsonfile)) > 0:
        with open(jsonfile) as json_file:
            data = json.load(json_file)
        keys = data.keys()
        latesthtmldict = {}
        for key in keys:
            k = f'<a href="{key}">{key}</a>'
            latesthtmldict[k] = data[key]
        name = jsonfile.split('.')
        htmltabel = json2html.convert(
            json=latesthtmldict, escape=False)  # type: ignore
        writefile = open(f"{name[0]}.html", "w")
        writefile.write("<center>"+htmltabel+"</center></div>")  # type: ignore
        writefile.close()
        os.system(f"start {name[0]}.html")


def deviant_scrapper_pages(self, baseurl: str, nextpage: int = 2) -> list:
    '''

        :param str baseurl:  Deviant art page url
        :param int nextpage:  Number of pages to visit
        :return: - list of all the art page links
        :rtype: list

        | Accepts a deviant url and searches for the sub deviant art links
        | Then next page cursor is searched and the function is called again with the next page url
        | each page returns 24 links, then 24*nextpage links will be returned
        | so if nexpage is 2 then 48 links are returned

        .. role:: raw-html(raw)
           :format: html

        .. deprecated:: 0.0.1
            :raw-html:`<br />`
            **Use :func:`deviantartapi.selenium_scrapper` instead
            outdated since Deviantart changed their website and introduced login system**


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
    nexts = urlextractor.next_cursor_requests(baseurl, page_cookie)
    while NextBtnClicker <= nextpage-1 and nexts:

        joinedurl = "https://www.deviantart.com"+nexts
        print(f"Accessing page {NextBtnClicker+1} = {joinedurl}....")
        main_page = requests.get(joinedurl, cookies=page_cookie)
        mp_cookie = main_page.cookies
        soup = BeautifulSoup(main_page.content, 'html.parser')
        for deviantdata in soup.findAll('div', {'class': "mWr4e"}):
            hrefval = deviantdata.select(
                'a[data-hook="deviation_link"]')[0]['href']
            deviantartpages.append(hrefval)
        nexts = urlextractor.next_cursor_requests(joinedurl, mp_cookie)
        NextBtnClicker += 1
        sleep(2)

    return deviantartpages
