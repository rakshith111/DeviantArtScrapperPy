# CHANGELOG

Any notable changes to this project that I deem necessary will be documented in this file.

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
- Need to find a way to login to the website.
```

## 0.0.1 - 22/11/2022

- Changed the way the program is structured. Now it is a module, and the main program is in the `main.py` file.
- Add sphinx doc gen 
- Updated Documentation
- Generate Documentation (docs/build/html)
- Updated File initialization