import streamlit as st

import json

from bokeh.io import output_file, show
from bokeh.models import GeoJSONDataSource,ColumnDataSource, OpenURL, TapTool
from bokeh.plotting import figure

import pandas as pd
import requests
import re
st.header('Pick a weather file')


r = requests.get('https://raw.githubusercontent.com/NREL/EnergyPlus/develop/weather/master.geojson')
data = r.json()


output_file("WeatherLocations.html")

for i in range(len(data['features'])):
    data['features'][i]['properties']['Color'] = ['blue', 'red'][i%2]

geo_source = GeoJSONDataSource(geojson=json.dumps(data))

TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select"

TOOLTIPS = [
    ('City:', '@title'), ('EPW:','@epw'), ('LAT and LONG:','@dir')
]

p = figure(x_range = (-180,180),y_range=(-90, 90),height=500, width = 1000, background_fill_color=None, tooltips=TOOLTIPS, tools = TOOLS)
p.image_url(url=['/World_location_map_equirectangular_180_No_Borders.svg'], x=-180, y=90, w=360, h=180)
p.circle(x='x', y='y', size=15, color='Color', alpha=0.3, source=geo_source)

taptool = p.select(type=TapTool)
RAWurl = "@epw"



text = RAWurl

front = re.compile('<a href=')
end =  re.compile('>Download Weather File</a>')
text = re.sub(front, '', text)

text = re.sub(end, '', text)


url = text
taptool.callback = OpenURL(url= url)

st.bokeh_chart((p), use_container_width=True)

#show(p)













