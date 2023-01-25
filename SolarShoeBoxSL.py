
import streamlit as st
from datetime import timedelta
import time
import pandas as pd
from io import StringIO
import numpy as np
import csv
from bokeh.palettes import Inferno
from bokeh.plotting import figure, show
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool,Slope, BoxAnnotation,DatetimeTickFormatter
from bokeh.models import LinearAxis, Range1d
from PIL import Image
import math

def gettey(nub):
    time.sleep(nub)


def plotWeather():
   TOOLS="hover,crosshair,reset,save"
   TOOLTIPS = [("value", "$y")]    
   hourData = list(range(0,x*60*60*1000, 60*60*1000))
   y1 = temperatureN
   y2 = GHI
   y3 = DNI
   y4 = DIFF
   y5 = clLow80day
   y6 = clHigh80day
   
   # create a new plot with a title and axis labels
   plotcomp= figure( y_range=(-30, 60),height=300, width = 700, tools=TOOLS, toolbar_location= 'above', tooltips = TOOLTIPS,
            x_axis_location="above",title = "Climate Data", x_axis_type="datetime",
           background_fill_color="white", x_range=(hourData[0], hourData[x-1]))

   plotcomp.extra_y_ranges = {"solar": Range1d(start=0, end=1400)}
   #plotcomp.add_layout(LinearAxis(y_range_name="solar"), 'right')

   # add multiple renderers
   plotcomp.xaxis.formatter = DatetimeTickFormatter(hours=["%H"],
                                                 days=["%d %b"],
                                                 months=["%d %b"])
                                                
   plotcomp.line(hourData, y2, legend_label="GHI", color="green", line_width=2, line_alpha = 0.8, y_range_name="solar")
   plotcomp.line(hourData, y3, legend_label="DNI", color="blue", line_width=2, line_alpha = 0.6 , y_range_name="solar")
   
   plotcomp.line(hourData, y4, legend_label="DHI", color="red", line_width=2, line_alpha = 0.6, y_range_name="solar" )                                              
   plotcomp.line(hourData, y5, legend_label="Lower Comfort", color="blue", line_width=4, line_alpha = 0.2 )
   plotcomp.line(hourData, y6, legend_label="Upper Comfort", color="red", line_width=4, line_alpha = 0.2 )

   plotcomp.line(hourData, y1, legend_label="Outdoor Air Temp", color="red", line_width=2)

   
   
   
   plotcomp.yaxis.axis_label = 'Temperature °C'
   plotcomp.add_layout(LinearAxis(y_range_name="solar", axis_label='Solar Radiation W/m2'), 'right')
   plotcomp.legend.orientation = "horizontal"
   plotcomp.legend.location = "top_center"
   plotcomp.legend.click_policy="hide"
   plotcomp.legend.label_text_font_size = '10px'
   plotcomp.legend.background_fill_alpha = 0.0
   plotcomp.legend.label_height = 12
   
   select = figure(title="Drag the middle and edges of the selection box to change the range above",
               height=100, width = plotcomp.width, y_range=plotcomp.y_range,
                x_axis_type="datetime", y_axis_type=None,
               tools="", toolbar_location=None, background_fill_color="#efefef")

   range_tool = RangeTool(x_range=plotcomp.x_range)
   range_tool.overlay.fill_color = "navy"
   range_tool.overlay.fill_alpha = 0.2

   select.line(hourData, y1)
   select.line(hourData, y5)
   select.line(hourData, y6)
   # select.line(hourData, y4)
   select.xaxis.formatter = DatetimeTickFormatter(hours=["%H"],
                                                 days=["%d %b"],
                                                 months=["%d %b"])
   select.ygrid.grid_line_color = None
   select.add_tools(range_tool)
   select.toolbar.active_multi = range_tool



   st.bokeh_chart(column(plotcomp, select), use_container_width= False)
   
def Ave_Daily_AirTemp():
    
    for j in range(0,365):
        Tave = 0
        for k in range(0,24):
            i = (24*j) + k
            Tave = temperatureN[i] + Tave
        aveDailyTemp.append(Tave/24)
        #print(round(aveDailyTemp[j],1))
    #print('end')
        
            

        
def running_mean_outdoor_temperature(temp_array, alpha=0.8): #this code is taken from pythermalcomfort library

    for i in range(0,365):
        if i < 6:
            temp_array7 = temp_array[0:i+1]
        else:
            temp_array7 = temp_array[i-6:i+1]
        coeff = [alpha ** ix for ix, x in enumerate(temp_array7)]
        t_rm = sum([a * b for a, b in zip(coeff, temp_array7)]) / sum(coeff)
        #print(sum([a * b for a, b in zip(coeff, temp_array7)]))
        runSevenDay.append(t_rm)
        #print(round(runSevenDay[i],1))
    #print('end2')

    




def adaptive_ashrae(t_running_mean):
    for i in range(0,365):
        t_running_mean = runSevenDay[i]
        if 10.0 <= t_running_mean <= 33.5:
            t_cmf = 0.31 * t_running_mean + 17.8
            tmp_cmf_80_low = t_cmf - 3.5
            tmp_cmf_90_low = t_cmf - 2.5
            tmp_cmf_80_up = t_cmf + 3.5 + 2.2
            tmp_cmf_90_up = t_cmf + 2.5 + 2.2

        elif t_running_mean < 10:
            t_cmf = 0.31 * 10 + 17.8
            tmp_cmf_80_low = t_cmf - 3.5
            tmp_cmf_90_low = t_cmf - 2.5
            tmp_cmf_80_up = t_cmf + 3.5
            tmp_cmf_90_up = t_cmf + 2.5

        else:
            t_cmf = 0.31 * 33.5 + 17.8
            tmp_cmf_80_low = t_cmf - 3.5
            tmp_cmf_90_low = t_cmf - 2.5
            tmp_cmf_80_up = t_cmf + 3.5 + 2.2
            tmp_cmf_90_up = t_cmf + 2.5 + 2.2 
                
                
        results = {
            
            "tmp_cmf_80_low": tmp_cmf_80_low,
            "tmp_cmf_80_up": tmp_cmf_80_up,
            "tmp_cmf_90_low": tmp_cmf_90_low,
            "tmp_cmf_90_up": tmp_cmf_90_up,
            "tmp_cmf_mid": t_cmf
    }
    

        clLow80.append(results['tmp_cmf_80_low'])
        clHigh80.append(results['tmp_cmf_80_up'])
        
        clLow90.append(results['tmp_cmf_90_low'])
        clHigh90.append(results['tmp_cmf_90_up'])
        clMid.append(results['tmp_cmf_mid'])    

def parameter_change():
    st.sidebar.write('Parameters Changed you must rerun simulation')

st.set_page_config(
    page_title="SolarShoeBox",
    page_icon='SolarShoeBoxSmall.jpg',
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'http://www.solarshoebox.com',
        'Report a bug': 'http://www.solarshoebox.com',
        'About': '**SolarShoeBox** design a **passive solar house** with predictive modelling for *shading* and *ventilation*. For more information about this subject please go to www.solarshoebox.com and read the latest news. This program was created by **Dr. Troy Nolan Peters** . You are free to use the information for non comercial use.'
    }
)

RSliderHelpText = 'This is a really long text to illustrate \nhow long this text will be in real ife. \nI dont have much to say about this right now \nbut all will be for gotten'

WeatherFileUploaderHelp ='Download weather file to your computer and drag/drop file to uploader.'

with st.sidebar.form("parameters_form"):
   st.write('Building Parameters')
   
   
   # values = st.slider(
    # 'Rotation from South',
    # -90, 90, (0), key=0, step = 5)
   # #st.write('Values:', values)
   

   Building_Area_Slide = st.slider(
    'Building Area (m2)',
    23, 120, (75), key=1, step = 1)
   #st.write('Values:', values3)
   
   R_Value_Slide = st.slider(
    'Whole Building R-value',
    6, 14, (9), key=2, step = 1, help=RSliderHelpText)
   #st.write('Values:', values1)

   Percent_South_Slide = st.slider(
    'Percent South Glazing',
    5, 90, (25), key=3, step = 5)
   #st.write('Values:', values2)

   option = st.selectbox(
    'Select Window Type:',
    ('Double','Triple'))
    
   Percent_South_Slide = st.slider(
    'Mass Thickness (cm)',
    0.5, 1.5 ,(1.0), key=4, step = 0.5)
   #st.write('Values:', values2)


   #st.write('Window Type:', option)

   submitted = st.form_submit_button("Run Simulation")
   if submitted:
       with st.spinner("Calculating..."):
           gettey(3)
           st.success("Done!")
       

col1,col2 = st.columns([2,1])
image = Image.open('SolarShoeBox.png')

col2.image(image, caption= None)

col1.markdown('# SolarShoeBox #')
col1.markdown('design a **passive solar house** with predictive modelling for *shading* and *ventilation*')

col3,col4 = st.columns([2,1])
col4.markdown('**Start Here:** Download weather file to your computer and drag/drop file to uploader or browse system for file.')
#col4.markdown('[Energyplus Weather](https://energyplus.net/weather)')



uploaded_file = col3.file_uploader('Upload Energyplus Weather File. File type must be .epw https://energyplus.net/weather', type= 'epw', help = WeatherFileUploaderHelp)
if uploaded_file is not None:

    
    header=8
    Weather_data = np.genfromtxt(uploaded_file, skip_header=header, delimiter=',')
    datalength=Weather_data[:]
    x=len(datalength)
    s=0

    monthN=Weather_data[s:x, 1]
    dayN=Weather_data[s:x, 2]
    hourN=Weather_data[s:x, 3]
    temperatureN=Weather_data[s:x, 6]
    GHI=Weather_data[s:x, 13]
    DNI=Weather_data[s:x, 14]
    DIFF=Weather_data[s:x, 15]
    CloudCover=Weather_data[s:x, 22]
    #Add running mean and comfort lines here
    aveDailyTemp = []
    runSevenDay =[]
    clLow80 = []
    clHigh80 = []
    clLow90 = []
    clHigh90 = []
    clMid =[]
    clLow80day = []
    clHigh80day = []
    Ave_Daily_AirTemp()
    running_mean_outdoor_temperature(aveDailyTemp, alpha=0.8)
    adaptive_ashrae(runSevenDay)
    for i in range(0, x):
        j= math.floor(i/24.0)
        clLow80day.append(clLow80[j])
        clHigh80day.append(clHigh80[j])
    plotWeather()

