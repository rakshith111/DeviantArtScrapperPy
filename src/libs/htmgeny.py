from json2html import *
import json
import os


def htmlgen(jsonfile) -> None:
    """
    :param str jsonfile: json file name(path)

    :return: None

    .. deprecated:: 0.0.1
        Only kept as a reference as pandas will use different methods


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
        htmltabel = json2html.convert(json=latesthtmldict, escape=False)
        writefile = open(f"{name[0]}.html", "w")
        writefile.write("<center>"+htmltabel+"</center></div>")
        writefile.close()
        os.system(f"start {name[0]}.html")
