import json,os,pickle

class extract:
    visited=[]
    failedlinks=[]
    data_keys=[]
    def __init__(self) -> None:
        '''
        links.pkl:consists of previously visited deviantart page links so that they arent visited more than once
        failed.pkl:contains steam links which failed to get steam price due to naming or unknown error 
        data.json: contains all visited steam links with prices , if the steam link appears again in another art page its price will be updated
        
        
        '''
        #check if files exists or not and create it
        if (not os.path.isfile('links.pkl')):
            with open('links.pkl', 'wb') as fp:
                init=["Blank","Blank1"]
                pickle.dump(init, fp)
        if (not os.path.isfile('failed.pkl')):
            with open('failed.pkl', 'wb') as fp:
                init=["https://steamcommunity.com/market/listings/753/447850-Void","https://steamcommunity.com/market/listings/753/554660-Puzzle%20Poker%20Card"]
                pickle.dump(init, fp)
        if (not os.path.isfile('data.json')):
            with open('data.json', 'w') as fp:
                fp.write(json.dumps({"LINKS": "values"}))
        #if files exist retrieve data
        with open('links.pkl', "rb") as txtfile:
            self.visited = pickle.load(txtfile)
        with open('failed.pkl', "rb") as txtfile:
            self.failedlinks = pickle.load(txtfile)        
        with open('data.json') as json_file:  
            data = json.load(json_file)                                              
        self.data_keys=data.keys()