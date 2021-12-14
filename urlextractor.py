import re
from time import sleep
import requests
from lxml import html
def urlextractor(url):
    try:
        page = requests.get(url)
        sleep(0.5)
        pagedata=html.fromstring(page.content)
        nextpage=pagedata.xpath('//*[text()="Next"]//@href')
        return nextpage[0]
    except IndexError:
        nextpage=[]
        nextpage.append(int(1))
        return nextpage
