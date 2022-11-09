from time import sleep
import requests
from lxml import html
#from random import randint
from requests import cookies

def nextcursor(baseurl, cookie):
    '''
    Accepts a deviant url along with its parent cookie, searches for the next page cursor , and returns the cursor part 
    if no next page  or any other error returns 0
    :param baseurl: str - Deviant art page url
    :param cookie: cookie - cookie of the parent page
    :return: str - next page cursor ex- "/tag/steamprofile?cursor=MTQwYWI2MjA9NCY1OTBhY2FkMD03MiZkMTc0YjZiYz1OJTJGQQ"
    '''
    try:
        page = requests.get(baseurl,cookies=cookie)
        sleep(0.5)
        pagedata=html.fromstring(page.content)
  
        nextpage=pagedata.xpath('//*[text()="Next"]//@href')
        return nextpage[0]
    except IndexError:
       return 0
       
def remove_filter(steamurl):
  posifilter = steamurl.find('?filter')
  if posifilter == -1:
    return steamurl
  return steamurl[:posifilter]