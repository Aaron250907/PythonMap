import streamlit as st
import folium
import requests
from streamlit_folium import st_folium

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Corruption Map", layout="wide")

st.title("🌍 Global Corruption Map (Highlighted Countries)")
st.write("Hover or click the highlighted countries to view their CPI score.")

# ---- LOAD WORLD GEOJSON ----
@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    return requests.get(url).json()

world_geojson = load_geojson()

# ---- CPI DATA (ONLY 3 COUNTRIES) ----
cpi_data = {
    "Portugal": 63,
    "India": 39,
    "Pakistan": 28
}

highlight_colors = {
    "Portugal": "#1e3a8a",   # Blue
    "India": "#e76f51",       # Saffron
    "Pakistan": "#0f5132"     # Green
}

default_color = "#d4d4d4"
border_color = "#333333"

# ---- CREATE MAP ----
m = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodbpositron")

# ---- STYLE FUNCTION ----
def style_function(feature):
    country = feature["properties"]["name"]

    if country in highlight_colors:
        return {
            "fillColor": highlight_colors[country],
            "color": highlight_colors[country],
            "weight": 2,
            "fillOpacity": 0.85
        }

    return {
        "fillColor": default_color,
        "color": border_color,
        "weight": 0.5,
        "fillOpacity": 0.5
    }

# ---- POPUP & TOOLTIP ----
def generate_popup(country_name):
    score = cpi_data.get(country_name, "No CPI Data")
    return folium.Popup(
        f"<b>{country_name}</b><br>CPI Score: {score}",
        max_width=250
    )

def generate_tooltip(country_name):
    score = cpi_data.get(country_name, "No CPI Data")
    return f"{country_name} — CPI: {score}"

# ---- ADD COUNTRIES ----
for feature in world_geojson["features"]:
    country = feature["properties"]["name"]

    folium.GeoJson(
        feature,
        style_function=style_function,
        tooltip=generate_tooltip(country),
        popup=generate_popup(country)
    ).add_to(m)

# ---- LEGEND ----
legend_html = """
<div style="
position: fixed; bottom: 30px; left: 30px; 
background: white; padding: 12px 15px;
border-radius: 8px; 
box-shadow: 0 4px 12px rgba(0,0,0,0.25);
font-size: 14px; line-height: 1.5;
">
<b>Highlighted Countries</b><br>
<span style='color:#1e3a8a;'>■</span> Portugal (63)<br>
<span style='color:#e76f51;'>■</span> India (39)<br>
<span style='color:#0f5132;'>■</span> Pakistan (28)
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# ---- DISPLAY MAP ----
st_folium(m, width=1100, height=600)
