from json2html import *
import json
import os
def htmlgen(jsonfile):
    """
    Generates and opens a html file for the given jsonfile
  
    Parameters:
    jsonfile (filepath): should be a path to file 
    Result:
    A html page is generated and opened 
    Note: A defualt brower must be set by windows 
    """
    with open(jsonfile) as json_file:  
        data =json.load(json_file) 
    keys=data.keys()
    newhtmldict={}
    for key in keys:
        k=f'<a href="{key}">{key}</a>'
        newhtmldict[k]=data[key]
    name=jsonfile.split('.')
    htmltabel = json2html.convert(json = newhtmldict,escape=False)
    writefile= open(f"{name[0]}.html","w")
    writefile.write("<center>"+htmltabel+"</center></div>")
    writefile.close()
    os.system(f"start {name[0]}.html")
