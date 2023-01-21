# CHANGELOG

Any notable changes to this project that I deem necessary will be documented in this file.

## 0.1.0 - 21/1/2023

- Renamed `steamget.py` to `steamapi.py`
- Optimized `main.py`'s init and file reload functions ( now more readable !!)
- `htmlgeny.py` now also generates a checkbox for each item which can be used to check whether the item has been visited or not
- Added `visitor.js` this is a script that will be injected into the html file to track whether the user has visited the page or not

## 0.0.9 - 21/1/2023

- Added Support for normal link(href)
- Added SteamCardExchange redirector
- Now shows sparated data i.e Empty data from real data
- Fixed 'None' return type for steam price (returns the `get_item(url)` function which calls it again)

## 0.0.8 -17/1/2023

- Moved Old html generater to `oldlibs.py`
- html generator now uses `Streamlit` to generate the html file
- htmlgeny runs separately from the main program now
- <s>Added a new `HtmlGeny` to `main.py` to use the new html generator </s>
- Added minimilistic UI to the html generator and table sorter

## 0.0.7 - 6/1/2023

```{important}

- Script runs fine now, further testing is required
- More analytical features will be added in the future

```

- Removed the slow typing feature, it was causing the program to fail (Thats my best guess as to why it was failing)
- Added a few options to the program

## 0.0.6 -3/1/2023

```{warning}

- <s>New anti selenium detection deployed by deviant art, now the program will fail at login</s>
- <s>Need to find a way to bypass the new anti selenium detection</s>
- <s>Halted development for now till I find a way to bypass the selenium detection</s>

```

- Added a new login method to fix cookie expire/ failures

## 0.0.5 - 25/12/2022

- Updated `main.py` to use all the modules and scrap the website
- Fixed an issue where the login failes due to expired cookies
- Now slow mode is enabled by default to avoid getting flagged as bot

## 0.0.4 - 24/12/2022

- Added steam price fetecher
- Saves the steam price to a file
- Updated module `steam_price.py` to fetch the steam price

## 0.0.3 - 16/12/2022

- Update the way the links are checked for redundancy, now it uses a `set` instead `in`
- Split the library documentation based on modules rather than one long file

## 0.0.2 - 04/12/2022

- Added Headless option for firefox
- Optimized searching for steam links using regex instead of string matching
- Modified the data files
- Writes steam links to file

## 0.0.2 - 01/12/2022

```{important}

- Added a login feature to the scrapper
- Since a login is required to access the full gallery, the scrapper will now ask for a username and password
```

- Now module uses selenium to scrape the website
- Selenuim firefox driver is used
- Other minor changes

## 0.0.1 - 29/11/2022

```{Warning}
DeviantArt Website Changes they added a login system to the website, which kinda broke the scraper.
- <s>Need to find a way to login to the website.</s>
```

## 0.0.1 - 22/11/2022

- Changed the way the program is structured. Now it is a module, and the main program is in the `main.py` file.
- Add sphinx doc gen
- Updated Documentation
- Generate Documentation (docs/build/html)
- Updated File initialization
