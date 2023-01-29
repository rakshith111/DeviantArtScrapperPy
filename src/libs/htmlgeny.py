import shutil
import os
import pathlib
import hashlib

import streamlit as st
import pandas as pd

from streamlit.components.v1 import html


class HtmlGeny:
    def __init__(self) -> None:
        '''
        Initiate the class and creates a copy of the sort-table.js and visitor.js files in the streamlit static folder

        '''
        streamlit_jspath = pathlib.Path(
            st.__path__[0]) / 'static' / 'static' / 'js'

        sort_table_js_path = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), "scripts", "sort-table.js")
        visitor_js_path = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), "scripts", "visitor.js")
        self.css_path = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), "scripts", "style.css")
        target_sort_table_js_path = streamlit_jspath / 'sort-table.js'
        target_visitor_js = streamlit_jspath / 'visitor.js'

        files_to_check = [(sort_table_js_path, target_sort_table_js_path),
                          (visitor_js_path, target_visitor_js)]
        for file_pair in files_to_check:
            if os.path.exists(file_pair[1]):
                print(f'[+] {file_pair[1]} exists')
            else:
                print(f'[x] {file_pair[1]} does not exist')
                shutil.copy(file_pair[0], streamlit_jspath)
                print(f'[+] {file_pair[1]} copied')
        st.set_page_config(
            layout="wide", page_title="Steam Deviant Price Checker", page_icon="🎮")
        st.title('Results')
        st.title("Steam Prices")

    def add_check_box(self, steam_url: str, length=6) -> str:
        '''
        :param str steamurl: steamurl of the game
        :param int length: length of the hash default is 6
        :rtype: str
        :example: add_check_box("https://steamcommunity.com/market/listings/753/470260-Lower%20deck")
        :return: <input type="checkbox" data-id="a395d9">

        | Takes a steamurl and returns a checkbox with data-id as the hash of the steamurl
        | using the data-id  for a persistent checkbox via local storage

        '''
        hash = hashlib.sha1()
        hash.update(str(steam_url).encode("utf-8"))
        data_id = hash.hexdigest()[:length]
        return f'<input type="checkbox" data-id="{data_id}">'

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
            
    def generate_html(self, steam_data: pd.DataFrame, deviant_data: pd.DataFrame) -> None:
        '''
        :param pd.DataFrame steam_data: Steam data
        :param pd.DataFrame deviant_data: Deviant data
        :rtype: None
        :example: generate_html(steam_data, deviant_data)
        :return: None

        | Generates the html for the streamlit app
        | Uses the sort-table.js file to sort the tables
        | Uses the scripts/style.css file to style the tables
        | Creates a temporary dataframe where all the attributes are converted to clickable links using the `make_clickable()` function
        | then converts the dataframe to html and adds the sort-table.js and style.css files to the html
        | finally writes the html to the streamlit app

        '''

        

        to_outdata_steam_data = pd.DataFrame()
        to_outdata_steam_data['SteamUrl'] = steam_data['SteamUrl'].apply(
            self.make_clickable)
        to_outdata_steam_data["AppTag"] = steam_data['AppTag']
        to_outdata_steam_data["Visited"] = steam_data["SteamUrl"].apply(
            self.add_check_box)
        to_outdata_steam_data["SteamPrice"] = steam_data['SteamPrice']
        to_outdata_steam_data["SteamPriceDate"] = steam_data['SteamPriceDate']
        to_outdata_steam_data["CardExchangeMarket"] = steam_data['AppTag'].apply(
            self.make_clickable, market=True)
        to_outdata_steam_data.drop_duplicates(inplace=True)
        table_html = to_outdata_steam_data.to_html(
            escape=False, index=False, classes="js-sort-table visitor cool-theme")
        table_html = table_html.replace(
            '<th>SteamPrice</th>', '<th class="js-sort-number" >SteamPrice</th>')
        table_html = table_html.replace(
            '<th>Visited</th>', '<th class="js-sort-0" >Visited</th>')
        css_data = open(f"{self.css_path}", 'r').read()
        table_html = table_html + f'<style>{css_data}</style>'
        st.write(table_html, unsafe_allow_html=True)

        st.title("Deviant Data")
        empty_data = deviant_data[deviant_data["SteamUrl"].isnull()]
        full_data = pd.concat([deviant_data, empty_data]
                              ).drop_duplicates(keep=False)

        to_out_deviantdata = pd.DataFrame()
        to_out_deviantdata['DeviantUrl'] = full_data['DeviantUrl'].apply(
            self.make_clickable)
        to_out_deviantdata['SteamUrl'] = full_data['SteamUrl'].apply(
            self.make_clickable)
        table_html = to_out_deviantdata.to_html(
            escape=False, index=False, classes="js-sort-table cool-theme  table-arrows ")

        st.write(table_html, unsafe_allow_html=True)
        st.title("No Steam Data")
        to_out_deviantdata = pd.DataFrame()
        to_out_deviantdata['DeviantUrl'] = empty_data['DeviantUrl'].apply(
            self.make_clickable)
        to_out_deviantdata['SteamUrl'] = empty_data['SteamUrl'].apply(
            self.make_clickable)
        table_html = to_out_deviantdata.to_html(
            escape=False, index=False, classes="js-sort-table cool-theme table-arrows")

        st.write(table_html, unsafe_allow_html=True)

        html('''
        <script src='./static/js/sort-table.js'>
        </script>''')
        html('''
        <script src='./static/js/visitor.js'>
        </script>''')


if __name__ == "__main__":

    steam_data = pd.read_csv(os.path.join(os.path.dirname(
        os.path.dirname(__file__)), "data", "localprice.csv"))
    deviant_data = pd.read_csv(os.path.join(os.path.dirname(
        os.path.dirname(__file__)), "data", "deviantXsteam.csv")
    )
    HtmlGeny().generate_html(steam_data, deviant_data)
