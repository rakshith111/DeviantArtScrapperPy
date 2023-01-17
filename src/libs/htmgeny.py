import streamlit as st
import pandas as pd
from streamlit.components.v1 import html
import streamlit as st
import shutil
import os
import pathlib


class htmlGeny:
    def __init__(self)-> None:
        '''
        Initiate the class and Creates a copy of the table-sort.js file in the streamlit static folder

        '''
        streamlit_jspath = pathlib.Path(
            st.__path__[0]) / 'static' / 'static' / 'js'
        target_jspath = streamlit_jspath / 'table-sort.js'
        source_file = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), "scripts", "table-sort.js")
        self.css_path = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), "scripts", "style.css")

        if os.path.exists(target_jspath):
            print('[+] table-sort.js exists')
        else:
            print('[x] table-sort.js does not exist')
            shutil.copy(source_file, streamlit_jspath)
            print('[+] table-sort.js copied')

    def make_clickable(self, link:str) -> str:
        '''
        :param str link: link to be made clickable
        :rtype: str
        :example: make_clickable("https://steamcommunity.com/market/listings/753/746850-Chinatown" )
        :return: <a target="_blank" href="https://steamcommunity.com/market/listings/753/746850-Chinatown">https://steamcommunity.com/market/listings/753/746850-Chinatown</a>

        | Takes a link and returns a clickable link

        '''
        if pd.isna(link):
            text = "No link"
            link = " "
            return f'<br>{text}<br>'
        else:
            text = f"{link}"
            return f'<a target="_blank" href="{link}">{text}</a>'

    def generate_html(self, steamdata, deviantdata):
        '''
        :param pd.DataFrame steamdata: Steam data
        :param pd.DataFrame deviantdata: Deviant data
        :rtype: None
        :example: generate_html(steamdata, deviantdata)
        :return: None
        
        | Generates the html for the streamlit app
        | Uses the table-sort.js file to sort the tables
        | Uses the scripts/style.css file to style the tables
        | Creates a temporary dataframe where all the attributes are converted to clickable links using the `make_clickable()` function
        | then converts the dataframe to html and adds the table-sort.js and style.css files to the html
        | finally writes the html to the streamlit app
        
        '''

        st.set_page_config(layout="wide")
        st.title('Results')
        st.title("Steam Prices")

        to_outdata_steamdata = pd.DataFrame()
        to_outdata_steamdata['SteamUrl'] = steamdata['SteamUrl'].apply(
            self.make_clickable)
        to_outdata_steamdata["AppTag"] = steamdata['AppTag']
        to_outdata_steamdata["SteamPrice"] = steamdata['SteamPrice']
        to_outdata_steamdata["SteamPriceDate"] = steamdata['SteamPriceDate']
        tablehtml = to_outdata_steamdata.to_html(
            escape=False, index=False, classes="table-sort cont table-arrows ")
        cssdata = open(f"{self.css_path}", 'r').read()
        tablehtml = tablehtml + f'<style>{cssdata}</style>'
        st.write(tablehtml, unsafe_allow_html=True)
        st.title("Deviant Data")
        to_out_deviantdata = pd.DataFrame()
        to_out_deviantdata['DeviantUrl'] = deviantdata['DeviantUrl'].apply(
            self.make_clickable)
        to_out_deviantdata['SteamUrl'] = deviantdata['SteamUrl'].apply(
            self.make_clickable)
        tablehtml = to_out_deviantdata.to_html(
            escape=False, index=False, classes="table-sort cont  table-arrows ")


        st.write(tablehtml, unsafe_allow_html=True)
    
        html('''
        <script src='./static/js/table-sort.js'>
        </script>''')
