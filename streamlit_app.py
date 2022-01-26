import base64
import streamlit as st
import gen_wallpaper
import pandas as pd
import numpy as np
import pickle
import os
st.set_option("deprecation.showfileUploaderEncoding", False)

st.markdown("""
# Genshin Impact Stars Wallpaper Generator

Create wallpapers for your favourite Genshin Impact characters!

Use the download link at the bottom for the best image quality!

You can find the app code on GitHub [here](https://github.com/Ze1598/genshin-wallpapers).

Reach out to me on Twitter for feedback [@Ze1598](https://github.com/Ze1598).
""")


def load_data() -> dict:
    data_path = os.path.join(os.getcwd(), "static", "data", "data.csv")
    data = pd.read_csv(data_path)        
    data.sort_values(by = "Character", axis = "rows", inplace = True)
    return data


def encode_img_to_b64(img_name: str) -> bytes:
    """Given the name of a image file, load it in bytes mode, and convert it to a base 64 bytes object.
    """
    # https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806/19
    with open(img_name, "rb") as f:
        img = f.read()
        encoded_img = base64.b64encode(img).decode()

    return encoded_img


# Load the main DF with all art data
main_data = load_data()

# Dropdown to filter by operator rarity
char_selector = st.selectbox(
    "Choose the character",
    main_data["Character"]
)
filtered_data = main_data.query(f"Character == '{char_selector}'")

# TODO: use base colour from character data as default
colour_picker = st.color_picker("Optionally change the background colour", filtered_data.iloc[0, 2])

char_align = st.selectbox(
    "How do you want to align the character?",
    ["Centred", "Right", "Left"]
)

art_info = {
    "Name": filtered_data.iloc[0, 0],
    "Url": filtered_data.iloc[0, 1],
    "Colour": colour_picker,
    "BaseColour": colour_picker,
    "CharAlign": char_align
}
wallpaper_name = gen_wallpaper.wallpaper_gen(art_info)

# Display the image on the page
st.image(
    wallpaper_name, 
    width=None, 
    use_column_width="auto",
    caption="Wallpaper preview"
)

# Encode the image to bytes so a download link can be created
encoded_img = encode_img_to_b64(wallpaper_name)
href = f'<a href="data:image/png;base64,{encoded_img}" download="{wallpaper_name}">Download the graphic</a>'
# Create the download link
st.markdown(href, unsafe_allow_html=True)

# Delete the graphic from the server
os.remove(wallpaper_name)
try:
    os.remove(wallpaper_name)
except:
    pass