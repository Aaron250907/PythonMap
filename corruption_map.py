import streamlit as st
import folium
import pandas as pd
import requests
from streamlit_folium import st_folium

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Global Corruption Map", layout="wide")

st.title("🌍 Global Corruption Perception Index (CPI) Map — 2024")
st.write("All countries are colored by CPI score (0 = highly corrupt, 100 = very clean).")
st.write("Portugal, India, and Pakistan are specially highlighted.")


# -------------------------
# LOAD CPI CSV
# -------------------------
@st.cache_data
def load_cpi():
    df = pd.read_csv("ti-corruption-perception-index.csv")
    df_2024 = df[df["Year"] == 2024].copy()
    df_2024 = df_2024[["Entity", "Code", "Year", "Corruption Perceptions Index"]]
    df_2024.rename(columns={"Entity": "Country", "Corruption Perceptions Index": "CPI"}, inplace=True)
    return df_2024

cpi_df = load_cpi()


# -------------------------
# LOAD WORLD GEOJSON
# -------------------------
@st.cache_data
def load_world_geojson():
    url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    return requests.get(url).json()

world_geojson = load_world_geojson()


# -------------------------
# HIGHLIGHT COLORS
# -------------------------
highlight_colors = {
    "Portugal": "#1e3a8a",
    "India": "#e76f51",
    "Pakistan": "#0f5132"
}

# -------------------------
# COLOR SCALE (Global)
# -------------------------
def cpi_to_color(cpi):
    if pd.isna(cpi):
        return "#cccccc"  # No data
    # Scale CPI: green (clean) to red (corrupt)
    import colorsys
    hue = (cpi / 100) * 0.33  # 0=red, 0.33=green
    r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
    return f"rgb({int(r*255)}, {int(g*255)}, {int(b*255)})"


# -------------------------
# HASH CPI FOR QUICK LOOKUP
# -------------------------
cpi_lookup = {row["Country"]: row["CPI"] for _, row in cpi_df.iterrows()}

# -------------------------
# CREATE MAP
# -------------------------
m = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodbpositron")


# -------------------------
# STYLE FUNCTION
# -------------------------
def style_function(feature):
    country = feature["properties"]["name"]
    cpi = cpi_lookup.get(country, None)

    # Highlight your 3
    if country in highlight_colors:
        return {
            "fillColor": highlight_colors[country],
            "color": highlight_colors[country],
            "weight": 2.5,
            "fillOpacity": 0.9
        }

    # Others get global CPI color
    return {
        "fillColor": cpi_to_color(cpi),
        "color": "#444444",
        "weight": 0.7,
        "fillOpacity": 0.7
    }


# -------------------------
# POPUP & TOOLTIP
# -------------------------
def make_popup(country):
    cpi = cpi_lookup.get(country, "No data")
    return folium.Popup(f"<b>{country}</b><br>CPI: {cpi}", max_width=250)


def make_tooltip(country):
    cpi = cpi_lookup.get(country, "No data")
    return f"{country} — CPI: {cpi}"


# -------------------------
# ADD GEOJSON LAYER
# -------------------------
for feature in world_geojson["features"]:
    country = feature["properties"]["name"]

    folium.GeoJson(
        feature,
        style_function=style_function,
        tooltip=make_tooltip(country),
        popup=make_popup(country)
    ).add_to(m)


# -------------------------
# LEGEND
# -------------------------
legend = """
<div style="
position: fixed; bottom: 30px; left: 30px;
background: white; padding: 12px 15px;
border-radius: 8px; font-size: 14px;
box-shadow: 0 4px 12px rgba(0,0,0,0.25);
">
<b>Highlighted Countries</b><br>
<span style='color:#1e3a8a;'>■</span> Portugal<br>
<span style='color:#e76f51;'>■</span> India<br>
<span style='color:#0f5132;'>■</span> Pakistan<br><br>

<b>CPI Scale</b><br>
<span style='color:rgb(255,0,0)'>■</span> Highly Corrupt (0)<br>
<span style='color:rgb(255,165,0)'>■</span> Medium (40)<br>
<span style='color:rgb(0,255,0)'>■</span> Very Clean (100)
</div>
"""
m.get_root().html.add_child(folium.Element(legend))


# -------------------------
# OUTPUT
# -------------------------
st_folium(m, width=1100, height=600)
