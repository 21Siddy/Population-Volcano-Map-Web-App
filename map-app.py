import folium
import pandas

data = pandas.read_csv("Volcanoes1.txt")
lat = list(data["Latitude"])
lon = list(data["Longitude"])
elev = list(data["Elev"])
name = list(data["Volcano Name"])


def color_seeker(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'


html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

map = folium.Map(location=[38.58, -99.09],
                 zoom_start=5, tiles="Stamen Terrain")
fgv = folium.FeatureGroup(name="Volcanoes")
for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=4, popup=folium.Popup(
        iframe), fill_color=color_seeker(el), color='grey', fill=True, fill_opacity=0.6))

fgt = folium.FeatureGroup(name="Population")
fgt.add_child(folium.GeoJson(
    data=open('world.json', 'r', encoding='utf-8-sig').read(),
    style_function=lambda x: {'fillColor': "green" if x['properties']['POP2005'] < 10000000
                              else "yellow" if 10000000 <= x['properties']['POP2005'] < 20000000 else "red"}))

map.add_child(fgv)
map.add_child(fgt)

map.add_child(folium.LayerControl())

map.save("Map_html_popup_advanced.html")
