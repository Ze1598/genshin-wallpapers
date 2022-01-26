from bs4 import BeautifulSoup
import pickle
import datetime
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
from colorthief import ColorThief
from io import BytesIO
logging.basicConfig(level=logging.INFO)

urls = [
    "https://genshin.mihoyo.com/en/character/mondstadt?char=0",
    "https://genshin.mihoyo.com/en/character/liyue?char=0",
    "https://genshin.mihoyo.com/en/character/inazuma?char=0"
]

# Use headless Chrome
chrome_options = Options()
chrome_options.headless = True
# Dynamically download and initialize a Chrome driver
driver = webdriver.Chrome(
    ChromeDriverManager().install(), 
    options = chrome_options
)
# Make the driver wait 7 seconds
driver.implicitly_wait(7)

# Running dictionary mapping character names to their art URL
chars_dict = dict()

# Scrape characters for each region
for url in urls:
    # Open the target URL
    driver.get(url)

    # Parse the source code
    soup = BeautifulSoup(driver.page_source, "lxml")
    
    # List of character art URLs
    char_arts = [char.img["src"] for char in soup.find("div", class_="character__main").div.ul.find_all("li")]
    # List of character names
    char_names  = [char.p.text for char in soup.find("div", class_="character__page").div.ul.find_all("li")]
    
    # Map names to art (they have the same order)
    chars_temp = {char: art for char, art in zip(char_names, char_arts)}
    
    # Merge the dictionary of this region to the running dictionary
    chars_dict = chars_dict | chars_temp

# Close now that we are finished scraping
driver.close()

# List of character names
characters = list(chars_dict.keys())
# List of their art URLs (based on the order stored in `characters`)
urls = [chars_dict[char] for char in characters]
# Generate a base colour for each character based on the most dominant colour in their art
colours = list()
for url in urls:
    img_req = requests.get(url)
    img_bytes = BytesIO(img_req.content)
    colour_thief = ColorThief(img_bytes)
    colour_chosen = colour_thief.get_palette(color_count=2)[0]
    colour_hex = f"#{colour_chosen[0]:02x}{colour_chosen[1]:02x}{colour_chosen[2]:02x}"
    colours.append(colour_hex)

data = pd.DataFrame({
    "Character": characters, 
    "Art": urls,
    "BaseColour": colours
})

# Output the results
data.to_csv("data.csv", index=False)