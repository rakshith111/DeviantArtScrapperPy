from time import sleep
import requests
from lxml import html
#from random import randint


def nextcursor_requests(baseurl: str, cookie) -> str:
    '''
    :param str baseurl:  Deviant art page url
    :param cookie cookie:  cookie of the parent page
    :return:  next page cursor 
    :rtype: str
    :example: "/tag/steamprofile?cursor=MTQwYWI2MjA9NCY1OTBhY2FkMD03MiZkMTc0YjZiYz1OJTJGQQ"

    .. deprecated:: 0.0.1
        Use :func:`deviantartapi.nextcursor_selenium` instead
        outdated since Deviantart changed their website and introduced login system
        Requests version doesn't render js

    | Made for requests version
    | Accepts a deviant url along with its parent cookie, searches for the next page cursor , and returns the cursor part 
    | if no next page  or any other error returns 0


    '''
    try:
        page = requests.get(baseurl, cookies=cookie)
        sleep(0.5)
        pagedata = html.fromstring(page.content)

        nextpage = pagedata.xpath('//*[text()="Next"]//@href')
        return nextpage[0]
    except IndexError:
        return 0


def nextcursor_selenium(page_data: str) -> str:
    '''


    :param str page_data: raw page source data of the page
    :return:  next page cursor 
    :rtype: str
    :exception: IndexError - if no next page  or any other error returns 0
    :example: "/tag/steamprofile?cursor=MTQwYWI2MjA9NCY1OTBhY2FkMD03MiZkMTc0YjZiYz1OJTJGQQ"

    | Made for selenuim version
    | Accepts a deviant page source , searches for the next page cursor , and returns the cursor part 
    | if no next page  or any other error returns 0


    '''
    try:
        sleep(0.5)
        pagedata = html.fromstring(page_data)
        nextpage = pagedata.xpath('//*[text()="Next"]//@href')
        return nextpage[0]
    except IndexError:
        return 0


def remove_filter(steamurl: str) -> str:
    ''' 
    :param str steamurl:  Steam url
    :return:  Steam url without filter tag
    :rtype: str

    | Accepts a steam url and removes the filter part of the url and returns the url
    | Some urls have a filter part which is not needed for the program to work, this function removes the filter part and returns the url
    | if no filter part is found returns the same url

    '''
    posifilter = steamurl.find('?filter')
    if posifilter == -1:
        return steamurl
    return steamurl[:posifilter]
