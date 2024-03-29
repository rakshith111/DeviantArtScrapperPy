% DeviantArtScrapper documentation master file, created by
% sphinx-quickstart on Tue Nov 22 01:21:58 2022.
% You can adapt this file completely to your liking, but it should at least
% contain the root `toctree` directive.

# Welcome to DeviantArtScrapper's documentation!

## Current version: 0.1.1

## About:

This is a python program which scrapes using `beautifulsoup4`,`selenim` and `requests` the deviantart website for popular steam artworks.
Then using the steam links, it fetches the steam price of the game and saves it to a file.
The program also generates a html file using `streamlit` with the data.

```{note}
Have an account on deviantart and be logged in.
Make sure you have the latest version of firefox installed as selenium uses it for logging in.
```
- Visit the [changelog](changelog.md) to know what's new in the latest version.
- Visit the [Modules](Modules.md) page to know more about the modules used in this program.
## Basic Usage:

- Install the requirements using `pip install -r requirements.txt`
- Run the program using `python main.py`
- Enter your deviantart username and password
- Wait for the program to finish
- The script will automatically open the html file in your default browser
- Visit the external links to view the artworks on steamcardexchange and steam and make your bet.
- 📈📈📈Enjoy!📈📈📈

### Optional:

- You can add new links to the `links.txt` file to scrape more artworks.
- You can change the number of links to check by changing the `links_to_scrape` variable in the `main.py` file. For example, if you want to scrape 10 links from the `links.txt`, change the `links_to_scrape` variable to 10.(Note: The links are scraped in the order they are in the `links.txt` file. Also make sure that the links are valid and are within the length of the file.)
- You can adjust the number of pages to visit by changing the `pages_to_check` variable in the `main.py` file. For example, if you want to visit 5 pages per link, change the `pages_to_check` variable to 5.



```{note}
Please note that this program is not affiliated with deviantart in any way.
This program is made for the sole purpose of learning and is not meant to be used for any other purpose.

```

```{note}
Please read the [To-do](To-do.md) list to know what features are planned for the future.
This is a work in progress. If you have any suggestions, please let me know.
```
[Mail](mailto:rakshithbabu111@gmail.com)
## Contents:
```{toctree}
:maxdepth: 1

Modules
```
```{toctree}
:maxdepth: 1
:caption: Reference
changelog
To-do
```
