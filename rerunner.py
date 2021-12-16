import pickle
import json

from steamget import get_item
from htmgeny import htmlgen
from urlextractor import remove_filter
new={}
from htmgeny import *

with open('failed.pkl', "rb") as txtfile:
    failedlinks = pickle.load(txtfile)
with open('data.json') as json_file:  
    data = json.load(json_file)
data_keys=data.keys()
print("\n Re-Running missed items\n\n")
if(len(failedlinks)>0):
    for link in failedlinks:
        link=remove_filter(link)
        try:
            price=get_item(link)
            if(not "NA" in price ):
                price=price.replace('₹','').replace(',','')
                price=float(price)
                if(price >=60.00):                                                 #Appends only if value is greater than 60
                    new[link]=price
                    data[link]=price
                failedlinks.remove(link)
                #data now has merged data from file and new appends to it 
                # Finally writing the data to file
                with open('new.json',"w",encoding='utf-8') as json_file:           
                    json_file.write(json.dumps(new))

        except TypeError: 
            failedlinks.append(link)
            print(link+" failed ")
            pass  
    with open('data.json',"w",encoding='utf-8') as json_file:                      
        json_file.write(json.dumps(data))
    with open('failed.pkl', "wb") as txtfile:                                        # Pickling the final links to file
        pickle.dump(failedlinks, txtfile)
    failedlinks=list(set(failedlinks))

htmlgen("data.json")
htmlgen("new.json")
print("Check new.html For Latest data")

