import streamlit as st
import pandas as pd
from streamlit.components.v1 import html
data = pd.read_csv('deviantXsteam.csv')

to_outdf = pd.DataFrame()


st.set_page_config(layout="wide")
st.title('Results')
st.set_page_config


def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    if pd.isna(link):
        text = "No link"
        link = " "
        return f'<a target="_blank" href="{link}">{text}</a>'
    else:
        text = f"{link}"
        return f'<a target="_blank" href="{link}">{text}</a>'


# link is the column with hyperlinks
to_outdf['DeviantUrl'] = data['DeviantUrl'].apply(make_clickable)
to_outdf['SteamUrl'] = data['SteamUrl'].apply(make_clickable)

to_outdf["price"] = data['price']
tablehtml = to_outdf.to_html(
    escape=False, index=False, classes="table-sort table-arrows")
st.write(tablehtml, unsafe_allow_html=True)

html('''
<script src='table-sort.js'>
</script>''')
