from time import sleep
import requests
from lxml import html
#from random import randint
def urlextractor(url,cookie):
    '''
    accepts a deviant url along with its parent cookie, searches for the next page cursor , and returns the cursor part 
    if no next page  or any other error returns 0
    '''
    print("FROM URL EX "+url)
    try:
        page = requests.get(url,cookies=cookie)
        #nu=randint(0,10)
        #print(f"writing {nu}")
        #open(f"asd{nu}.html",'wb').write(page.content)  
        sleep(0.5)
        pagedata=html.fromstring(page.content)
        nextpage=pagedata.xpath('//*[text()="Next"]//@href')
        return nextpage[0].split("&")[1]
    except IndexError:
       return 0
def remove_filter(steamurl):
  posifilter = steamurl.find('?filter')
  if posifilter == -1:
    return steamurl
  return steamurl[:posifilter]