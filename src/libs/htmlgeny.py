import streamlit as st
import pandas as pd
from streamlit.components.v1 import html
import shutil
import os
import pathlib
import hashlib


class htmlGeny:
    def __init__(self) -> None:
        '''
        Initiate the class and Creates a copy of the sort-table.js file in the streamlit static folder

        '''
        streamlit_jspath = pathlib.Path(
            st.__path__[0]) / 'static' / 'static' / 'js'

        table_sortjs = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), "scripts", "sort-table.js")
        visitorjs = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), "scripts", "visitor.js")
        self.css_path = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), "scripts", "style.css")
        target_jable_sortjs = streamlit_jspath / 'sort-table.js'
        target_visitorjs = streamlit_jspath / 'visitor.js'

        files_to_check = [(table_sortjs, target_jable_sortjs),
                          (visitorjs, target_visitorjs)]
        for file_pair in files_to_check:
            if os.path.exists(file_pair[1]):
                print(f'[+] {file_pair[1]} exists')
            else:
                print(f'[x] {file_pair[1]} does not exist')
                shutil.copy(file_pair[0], streamlit_jspath)
                print(f'[+] {file_pair[1]} copied')

    def addCheckbox(self, steamurl: str, length=6) -> str:
        '''
        :param str steamurl: steamurl of the game
        :param int length: length of the hash default is 6
        :rtype: str
        :example: addCheckbox("https://steamcommunity.com/market/listings/753/470260-Lower%20deck")
        :return: <input type="checkbox" data-id="a395d9">

        | Takes a steamurl and returns a checkbox with data-id as the hash of the steamurl
        | using the data-id  for a persistent checkbox via local storage

        '''
        hash = hashlib.sha1()
        hash.update(str(steamurl).encode("utf-8"))
        dataid = hash.hexdigest()[:length]
        return f'<input type="checkbox" data-id="{dataid}">'

    def make_clickable(self, link: str, market: bool = False) -> str:
        '''
        :param str link: link to be made clickable
        :param bool market: if true makes the text as just "LINK" and connects it to market
        :rtype: str
        :example: make_clickable("https://steamcommunity.com/market/listings/753/746850-Chinatown" )
        :return: <a target="_blank" href="https://steamcommunity.com/market/listings/753/746850-Chinatown">https://steamcommunity.com/market/listings/753/746850-Chinatown</a>

        | Takes a link and returns a clickable link

        '''
        if pd.isna(link):
            text = "No link"
            link = " "
            return f'<br>{text}<br>'
        if market:
            text = f"{link}"
            return f'<a target="_blank" href="https://www.steamcardexchange.net/index.php?gamepage-appid-{link}">LINK</a>'
        else:
            text = f"{link}"
            return f'<a target="_blank" href="{link}">{text}</a>'

    def generate_html(self, steamdata: pd.DataFrame, deviantdata: pd.DataFrame) -> None:
        '''
        :param pd.DataFrame steamdata: Steam data
        :param pd.DataFrame deviantdata: Deviant data
        :rtype: None
        :example: generate_html(steamdata, deviantdata)
        :return: None

        | Generates the html for the streamlit app
        | Uses the sort-table.js file to sort the tables
        | Uses the scripts/style.css file to style the tables
        | Creates a temporary dataframe where all the attributes are converted to clickable links using the `make_clickable()` function
        | then converts the dataframe to html and adds the sort-table.js and style.css files to the html
        | finally writes the html to the streamlit app

        '''

        st.set_page_config(
            layout="wide", page_title="Steam Deviant Price Checker", page_icon="🎮")
        st.title('Results')
        st.title("Steam Prices")

        to_outdata_steamdata = pd.DataFrame()
        to_outdata_steamdata['SteamUrl'] = steamdata['SteamUrl'].apply(
            self.make_clickable)
        to_outdata_steamdata["AppTag"] = steamdata['AppTag']
        to_outdata_steamdata["Visited"] = steamdata["SteamUrl"].apply(
            self.addCheckbox)
        to_outdata_steamdata["SteamPrice"] = steamdata['SteamPrice']
        to_outdata_steamdata["SteamPriceDate"] = steamdata['SteamPriceDate']
        to_outdata_steamdata["CardExchangeMarket"] = steamdata['AppTag'].apply(
            self.make_clickable, market=True)
        to_outdata_steamdata.drop_duplicates(inplace=True)
        tablehtml = to_outdata_steamdata.to_html(
            escape=False, index=False, classes="js-sort-table visitor cool-theme")
        tablehtml = tablehtml.replace(
            '<th>SteamPrice</th>', '<th class="js-sort-number" >SteamPrice</th>')
        tablehtml = tablehtml.replace(
            '<th>Visited</th>', '<th class="js-sort-0" >Visited</th>')
        cssdata = open(f"{self.css_path}", 'r').read()
        tablehtml = tablehtml + f'<style>{cssdata}</style>'
        st.write(tablehtml, unsafe_allow_html=True)

        st.title("Deviant Data")
        emptydata = deviantdata[deviantdata["SteamUrl"].isnull()]
        fulldata = pd.concat([deviantdata, emptydata]
                             ).drop_duplicates(keep=False)

        to_out_deviantdata = pd.DataFrame()
        to_out_deviantdata['DeviantUrl'] = fulldata['DeviantUrl'].apply(
            self.make_clickable)
        to_out_deviantdata['SteamUrl'] = fulldata['SteamUrl'].apply(
            self.make_clickable)
        tablehtml = to_out_deviantdata.to_html(
            escape=False, index=False, classes="js-sort-table cool-theme  table-arrows ")

        st.write(tablehtml, unsafe_allow_html=True)
        st.title("No Steam Data")
        to_out_deviantdata = pd.DataFrame()
        to_out_deviantdata['DeviantUrl'] = emptydata['DeviantUrl'].apply(
            self.make_clickable)
        to_out_deviantdata['SteamUrl'] = emptydata['SteamUrl'].apply(
            self.make_clickable)
        tablehtml = to_out_deviantdata.to_html(
            escape=False, index=False, classes="js-sort-table cool-theme table-arrows")

        st.write(tablehtml, unsafe_allow_html=True)

        html('''
        <script src='./static/js/sort-table.js'>
        </script>''')
        html('''
        <script src='./static/js/visitor.js'>
        </script>''')


if __name__ == "__main__":

    steamdata = pd.read_csv(os.path.join(os.path.dirname(
        os.path.dirname(__file__)), "data", "localprice.csv"))
    deviantdata = pd.read_csv(os.path.join(os.path.dirname(
        os.path.dirname(__file__)), "data", "deviantXsteam.csv")
    )
    htmlGeny().generate_html(steamdata, deviantdata)
