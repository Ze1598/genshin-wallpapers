# genshin-wallpapers
[live app](https://share.streamlit.io/ze1598/genshin-wallpapers/main)

A web app built with [Streamlit](https://www.streamlit.io/) in Python to create Genshin Impact desktop wallpapers on the fly.

The art was scraped from the [game's website](https://genshin.mihoyo.com/en/character/mondstadt?char=0) and images are loaded directly from their source. This scraping is done with [Selenium](https://selenium-python.readthedocs.io/), [requests](https://pypi.org/project/requests/) and [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) libraries.
The background colours are chosen dynamically by analysing the art and detecting the most dominant colour.