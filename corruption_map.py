import streamlit as st
import folium
import json
import requests
from streamlit_folium import st_folium

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Corruption Map",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Global Corruption Map (Highlighted Countries)")

st.write("""
This interactive map highlights **Portugal**, **India**, and **Pakistan** with special colors.  
Hover or click to view the CPI (Corruption Perception Index) score.
""")


# -----------------------------
# LOAD WORLD GEOJSON
# -----------------------------
@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    return requests.get(url).json()

world_geojson = load_geojson()


# -----------------------------
# CORRUPTION DATA
# -----------------------------
cpi_data = {
    "Portugal": 63,
    "India": 39,
    "Pakistan": 28
}

highlight_colors = {
    "Portugal": "#1e3a8a",   # Deep Blue
    "India": "#e76f51",       # Saffron
    "Pakistan": "#0f5132"     # Deep Green
}

default_color = "#cbd5e1"   # Light academic grey
border_color = "#111111"


# -----------------------------
# CREATE FOLIUM MAP
# -----------------------------
m = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodbpositron")


# -----------------------------
# STYLE FUNCTION
# -----------------------------
def style_function(feature):
    country = feature["properties"]["name"]

    if country in highlight_colors:
        return {
            "fillColor": highlight_colors[country],
            "color": highlight_colors[country],
            "weight": 2,
            "fillOpacity": 0.75
        }

    # Default styling for other countries
    return {
        "fillColor": default_color,
        "color": border_color,
        "weight": 1,
        "fillOpacity": 0.45
    }


# -----------------------------
# POPUP / TOOLTIP FUNCTION
# -----------------------------
def tooltip_function(feature):
    country = feature["properties"]["name"]
    score = cpi_data.get(country, "No data")
    return f"{country} — CPI: {score}"


# -----------------------------
# ADD LAYER
# -----------------------------
folium.GeoJson(
    world_geojson,
    name="Corruption Map",
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(
        fields=["name"],
        aliases=["Country:"],
        labels=True,
        sticky=True
    ),
    popup=folium.GeoJsonPopup(
        fields=["name"],
        aliases=["Country:"],
        labels=True
    )
).add_to(m)


# -----------------------------
# ADD LEGEND
# -----------------------------
legend_html = """
<div style="
position: fixed; 
bottom: 30px; left: 30px; width: 220px; 
background: white; padding: 12px; 
border-radius: 8px; font-size: 15px;
box-shadow: 0 4px 10px rgba(0,0,0,0.25);
">
<b>Highlighted Countries</b><br>
<span style='color:#1e3a8a;'>■</span> Portugal – CPI 63<br>
<span style='color:#e76f51;'>■</span> India – CPI 39<br>
<span style='color:#0f5132;'>■</span> Pakistan – CPI 28<br>
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))


# -----------------------------
# DISPLAY MAP
# -----------------------------
st_folium(m, width=1100, height=600)
