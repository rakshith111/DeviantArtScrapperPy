import json,os,pickle,re
from htmgeny import htmlgen
from urlextractor import remove_filter
from steamget import get_item
class scrapper:
    visited=set()
    data=dict()
    latest=dict()
    failedlinks=[]
    urls=[]
    data_keys=[]
    match_string="https://steamcommunity.com/market/listings/"
    remove_string="https://www.deviantart.com/users/outgoing?"
    
    def __init__(self) -> None:
        '''
        (visited)    links.pkl:consists of previously visited deviantart page links so that they arent visited more than once
        (failedlinks)failed.pkl:contains steam links which failed to get steam price due to naming or unknown error 
        (data)       data.json: contains all visited steam links with prices , if the steam link appears again in another art page its price will be updated
        (url)        links.txt: list of all the links to check with
        
        '''
        #check if files exists or not and create it
        if (not os.path.isfile('links.pkl')):
            with open('links.pkl', 'wb') as pf:
                init=["Blank","Blank1"]
                pickle.dump(init, pf)
        if (not os.path.isfile('failed.pkl')):
            with open('failed.pkl', 'wb') as pf:
                init=["https://steamcommunity.com/market/listings/753/447850-Void",
                      "https://steamcommunity.com/market/listings/753/554660-Puzzle%20Poker%20Card"]
                pickle.dump(init, pf)
        if (not os.path.isfile('data.json')):
            with open('data.json', 'w') as jf:
                jf.write(json.dumps({"LINKS": "values"}))
        #if files exist retrieve data
        with open('links.pkl', "rb") as file:
            self.visited = set(pickle.load(file))
        try:
            with open('failed.pkl', "rb") as file:
                self.failedlinks = pickle.load(file)    
        except EOFError: 
            self.failedlinks=list()    
        with open('data.json') as json_file:  
            self.data = json.load(json_file)                                              
            self.data_keys=self.data.keys()
        with open ("links.txt",'r') as file:
            self.urls=json.loads(file.read())

    def writer(self):
        with open('latest.json',"w",encoding='utf-8') as json_file:           
            json_file.write(json.dumps(self.latest))
        with open('data.json',"w",encoding='utf-8') as json_file:                      
            json_file.write(json.dumps(self.data))
        with open('failed.pkl', "wb") as txtfile:                                        
            pickle.dump(self.failedlinks, txtfile)
        with open('links.pkl', "wb") as txtfile:                                       
            pickle.dump(list(self.visited), txtfile)
    def rerunner(self):
        if(len(self.failedlinks)>0):
            print("\n Re-Running missed items\n\n")
            for link in self.failedlinks:
                link=remove_filter(link)

                
                try:
                    price=get_item(link)
                    if(not "NA" in price ):
                        price=float(re.findall("[\d,]+[\.][\d]+",price)[0])
                        if(price >=100.00):                                                 #Appends only if value is greater than 100
                            self.latest[link]=price
                            self.data[link]=price
                            self.failedlinks.remove(link)
                except TypeError:
                    self.failedlinks.append(link)
                    print(link+" failed ")
                    pass
        with open('data.json',"w",encoding='utf-8') as json_file:                      
            json_file.write(json.dumps(self.data))
        self.failedlinks=list(set(self.failedlinks))
        with open('failed.pkl', "wb") as file:                                        # Pickling the final links to file
            pickle.dump(self.failedlinks, file)
        htmlgen("data.json")
        htmlgen("latest.json")
        print("Check latest.html For Latest data")
        print("Done")