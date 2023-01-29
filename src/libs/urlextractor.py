import requests
from time import sleep
from lxml import html
# from random import randint



def next_cursor_selenium(page_data: str) -> str:
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
        page_data = html.fromstring(page_data)
        next_page = page_data.xpath('//*[text()="Next"]//@href')
        return next_page[0]
    except IndexError:
        return 0  # type: ignore


def url_cleaner(steam_url: str) -> str:
    ''' 
    :param str steamurl:  Steam url
    :return:  Steam url without filter tag
    :rtype: str

    | Accepts a steam url and removes the filter part of the url and returns the url
    | Some urls have a filter part which is not needed for the program to work, this function removes the filter part and returns the url
    | if no filter part is found returns the same url
    | Removes # from the url as well
    | converts http to https

    '''
    remove_stf=["#","]","["]
    for item in remove_stf:
        steam_url=steam_url.replace(item,"")
    steam_url="https://"+steam_url[steam_url.find("s"):]
    position_filter = steam_url.find('?')
    if position_filter == -1:
        return steam_url
    return steam_url[:position_filter]


def next_cursor_requests(base_url: str, cookie) -> str:
    '''
    :param str base_url:  Deviant art page url
    :param cookie cookie:  cookie of the parent page
    :return:  next page cursor 
    :rtype: str
    :example: "/tag/steamprofile?cursor=MTQwYWI2MjA9NCY1OTBhY2FkMD03MiZkMTc0YjZiYz1OJTJGQQ"

    | Made for requests version
    | Accepts a deviant url along with its parent cookie, searches for the next page cursor, and returns the cursor part 
    | if no next page  or any other error returns 0

    .. role:: raw-html(raw)
        :format: html

    .. deprecated:: 0.0.1
        :raw-html:`<br />`
        **Use :func:`deviantartapi.nextcursor_selenium` instead**
        outdated since Deviantart changed their website and introduced login system,also
        the requests version doesn't render js

    '''

    try:
        page = requests.get(base_url, cookies=cookie)
        sleep(0.5)
        pagedata = html.fromstring(page.content)

        nextpage = pagedata.xpath('//*[text()="Next"]//@href')
        return nextpage[0]
    except IndexError:
        return 0  # type: ignore
