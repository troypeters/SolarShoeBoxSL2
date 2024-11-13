
import streamlit as st
from datetime import timedelta
import time
import pandas as pd
from io import StringIO
import numpy as np
import csv
import codecs
from datetime import date
from datetime import time
from bokeh.palettes import Inferno
from bokeh.plotting import figure, show
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool,Slope, BoxAnnotation,DatetimeTickFormatter
from bokeh.models import LinearAxis, Range1d


from bokeh.io import show
from bokeh.models import CustomJS, DateRangeSlider

from PIL import Image
import math
import heapq



pi = math.pi
sin = math.sin
cos = math.cos
acos = math.acos
tan = math.tan
asin = math.asin
radians=math.radians
degrees=math.degrees
exp = math.exp
log=math.log


# Convert radians to degrees
rtd = 180/pi

# Convert degrees to radians
dtr = pi/180


def gettey(nub):
    time.sleep(nub)


def plotWeather():
   TOOLS="hover,crosshair,reset,save"
   TOOLTIPS = [("value", "$x,$y")]    
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





def plotSimpleWeather():
   TOOLS="hover,crosshair,reset,save"
   TOOLTIPS = [("value", "$y"), ('date', '$x')]    
   hourData = list(range(0,x*60*60*1000, 24*60*60*1000))
   y1 = aveDailyTemp
   y2 = aveDailyGHI
   y3 = aveDailySouthTrans
   #y4 = DIFF
   y5 = clLow80
   y6 = clHigh80
   y7 = runSevenDaySSolTrans
   y8 = runSevenDay
   
   
   TITLE = 'Climate Data for ', location, State,Country ,'Lat: ' ,latitude , 'Long: ' ,longitude
   # create a new plot with a title and axis labels
   plotcomp= figure( y_range=(-30, 60),height=300, width = 700, tools=TOOLS, toolbar_location= 'above', tooltips = TOOLTIPS,
            x_axis_location="above",title = "Climate Data", x_axis_type="datetime",
           background_fill_color="white", x_range=(hourData[0], hourData[365-1]))

   plotcomp.extra_y_ranges = {"solar": Range1d(start=0, end=500)}
   #plotcomp.add_layout(LinearAxis(y_range_name="solar"), 'right')

   # add multiple renderers
   plotcomp.xaxis.formatter = DatetimeTickFormatter(hours=["%H"],
                                                 days=["%d %b"],
                                                 months=["%d %b"])
                                                
   #plotcomp.line(hourData, y2, legend_label="Ave Daily GHI", color="red", line_width=3, line_alpha = 1.0, y_range_name="solar")
   #plotcomp.line(hourData, y3, legend_label="Ave Daily South Transmittance", color="blue", line_width=2, line_alpha = 0.6 , y_range_name="solar")
   
   #plotcomp.line(hourData, y4, legend_label="DHI", color="red", line_width=2, line_alpha = 0.6, y_range_name="solar" )                                              
   plotcomp.line(hourData, y5, legend_label="Lower Comfort", color="blue", line_width=4, line_alpha = 0.2 )
   plotcomp.line(hourData, y6, legend_label="Upper Comfort", color="red", line_width=4, line_alpha = 0.2 )

   #plotcomp.line(hourData, y1, legend_label="Average Daily Outdoor Air Temp", color="black", line_width=3)

   plotcomp.line(hourData, y8, legend_label="Average Daily Outdoor Air Temp", color="black", line_width=3)
   plotcomp.line(hourData, y7, legend_label="Ave Daily South Transmittance", color="blue", line_width=2, line_alpha = 0.6 , y_range_name="solar")

   
   
   
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
   range_tool.overlay.fill_color = "green"
   range_tool.overlay.fill_alpha = 0.1

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



   date_range_slider = DateRangeSlider(value=(date(2000, 4, 21), date(2000, 9, 21)),
                                    start=date(2000, 1, 1), end=date(2000, 12, 31), width = plotcomp.width, bar_color = 'red',format = '%d %b' )
   date_range_slider.js_on_change("value", CustomJS(code="""
    console.log('date_range_slider: value=' + this.value, this.toString())
     """))



   st.bokeh_chart(column(plotcomp,date_range_slider, select), use_container_width= False)
   
   appointment = st.slider("Select transition dates between heating and cooling:", value=(date(2000, 1, 15), date(2000, 12, 31)), format="MM/DD")
   st.write("Cooling months are between", appointment)

    
def day_number(month_of_year, day_of_month, Leap_Year=False):
    
    days_in_previous_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]    
    month_start_day = days_in_previous_month[0]
    j = month_of_year
    
    if Leap_Year == True:
        days_in_previous_month[2]= 29
    else:
        None
        
    if month_of_year < 1 or month_of_year > (len(days_in_previous_month)-1):
        return "Error - month must be an integer between 1 and " + str(len(days_in_previous_month)-1)
    else:
        if day_of_month < 1 or day_of_month > days_in_previous_month[j]:
            return "Error - day in month " + str(j) + " must be an integer between 1 and " + str(days_in_previous_month[j])
        else:
            for k in range(0, j):
                month_start_day = month_start_day + days_in_previous_month[k]
    
    return month_start_day + day_of_month

def leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    else:
        return False
#print(leap_year(2000))

    
def equation_of_time(day_number):
    if 1 <= day_number <=106:
        a=-14.2
        b=7
        c=111
    elif 107 <= day_number <=166:
        a=4
        b=106
        c=59
    elif 167 <= day_number <=246:
        a=-6.5
        b=166
        c=80
    elif 247 <= day_number <=365:
        a=16.4
        b=247
        c=113
    #return a*sin(pi*(day_number-b)/c)
    return 229.18*((0.0418*sin((4*pi*(day_number-4)/365.24)+3.5884)-0.0334*sin(2*pi*(day_number-4)/365.24)))

def eccentricity(day_number):
    day_angle  = 2*pi*(day_number-1)/365
    E0  = 1.00011+0.034221*cos(day_angle)+0.00128*sin(day_angle)+0.000719*cos(2*day_angle)+0.000077*sin(2*day_angle)
    return E0

def solar_declination(day_number):
    return 23.45 * sin( 2*pi/365 * (day_number + 284) )
    
def hour_angle(apparent_solar_time):
    return 180-(15 * (apparent_solar_time))

def apparent_solar_time(local_standard_time, longitude_of_site, equation_of_time, local_standard_time_meridian):
    return (local_standard_time)+(equation_of_time/60)+((local_standard_time_meridian-longitude)/15)-.5

def solar_altitude(
    solar_declination, 
    latitude, 
    hour_angle):
    sa= rtd*asin((sin(solar_declination*dtr) * sin(latitude*dtr)) + (cos(solar_declination*dtr) \
    * cos(latitude*dtr) * cos(hour_angle*dtr)))
    if sa<0:
        return 0
    else:
        return sa
        
# check for noon and sign before and after noon
def solar_azimuth(
    apparent_solar_time,
    solar_altitude,
    latitude, 
    solar_declination
    ):
    if solar_altitude <= 0:
        return 0
    elif apparent_solar_time == 12:
        return 0
    elif apparent_solar_time > 12:
        return -rtd*acos(((sin(solar_altitude*dtr) * sin(latitude*dtr)) \
        - sin(solar_declination*dtr)) / (cos(solar_altitude*dtr) * cos(latitude*dtr)))  
    else:
        return rtd*acos(((sin(solar_altitude*dtr) * sin(latitude*dtr)) \
        - sin(solar_declination*dtr)) / (cos(solar_altitude*dtr) * cos(latitude*dtr)))  

def AltiAzmi(LSTM, latitude, longitude, x):
    for i in range(0, x):
        dayNumber = math.floor(i/24)
        Day.append(dayNumber) #keep
        hourOfDay = i % 24              #keep
        Hour.append(hourOfDay)
        SD = solar_declination(dayNumber)
        ECC = eccentricity(dayNumber)
        ET = equation_of_time(dayNumber)
        AST = apparent_solar_time(hourOfDay, longitude, ET, LSTM)
        HA = hour_angle(AST)
        ALTITUDE = solar_altitude(SD, latitude, HA) #keep
        Altitude.append(ALTITUDE)
        AZIMUTH = solar_azimuth(AST,ALTITUDE,latitude, SD) #keep
        Azimuth.append(AZIMUTH)

def angle_of_incidence_of_sun(surface_tilt, angle_from_south, altitude_of_sun, azimuth_of_sun):
    
    zenith_A = 90- altitude_of_sun
    horizontal_angle_cos= cos(radians(azimuth_of_sun - angle_from_south))
    tilt_cos = cos(radians(surface_tilt))
    tilt_sin = sin(radians(surface_tilt))
    zenith_A_cos = cos(radians(zenith_A))
    zenith_A_sin = sin(radians(zenith_A))
    return degrees(acos((zenith_A_cos*tilt_cos)+(zenith_A_sin*tilt_sin*horizontal_angle_cos)))
    
 
def transCoeff(angle_of_incidence_of_sun):
    totalTransmittance = 1- tan(radians(angle_of_incidence_of_sun/2.0))**4
    return totalTransmittance
    
def transmitted_solar_radition(angle_of_incidence_of_sun, direct_normal, diffuse, surface_tilt):
    
    if angle_of_incidence_of_sun >= 90: 
        angle_of_incidence_of_sun = 90
    else:
        angle_of_incidence_of_sun = angle_of_incidence_of_sun
    transmittionCoef = transCoeff(angle_of_incidence_of_sun)
    incidence_cos = cos(radians(angle_of_incidence_of_sun))
    tilt_cos = cos(radians(surface_tilt))
    Fss = (1+tilt_cos)/2
    return (direct_normal*incidence_cos*transmittionCoef) + (diffuse * Fss)

def incident_solar_radition(angle_of_incidence_of_sun, direct_normal, diffuse, surface_tilt):
    
    if angle_of_incidence_of_sun >= 90: 
        angle_of_incidence_of_sun = 90
    else:
        angle_of_incidence_of_sun = angle_of_incidence_of_sun
    incidence_cos = cos(radians(angle_of_incidence_of_sun))
    tilt_cos = cos(radians(surface_tilt))
    Fss = (1+tilt_cos)/2
    return (direct_normal*incidence_cos) + (diffuse * Fss)

def sol_air_temp(T0, incident_solar_radiation, tiltangle):
    ah=.052 #.052, .026
    if tiltangle < 45:
        eRh=4
    else:
        eRh=0
    solair=T0+(incident_solar_radiation*ah)-eRh
    return solair

        

    
    
def GlazingRadTrans(surface_tilt, angle_from_south, x):
    for i in range(0, x):
        angleOfIncidence = angle_of_incidence_of_sun(surface_tilt, angle_from_south, Altitude[i], Azimuth[i])
        TransSolRad = transmitted_solar_radition(angleOfIncidence, DNI[i], DIFF[i], surface_tilt)
        SouthGlazingRadTrans.append(TransSolRad)
        

def Ave_Daily_AirTemp():
    
    for j in range(0,365):
        Tave = 0
        for k in range(0,24):
            i = (24*j) + k
            Tave = temperatureN[i] + Tave
        aveDailyTemp.append(Tave/24)

def Ave_Daily_GHI():
    
    for j in range(0,365):
        GHIave = 0
        for k in range(0,24):
            i = (24*j) + k
            GHIave = GHI[i] + GHIave
        aveDailyGHI.append(GHIave/24)
            
def Ave_Daily_SouthTrans():
    
    for j in range(0,365):
        SouthTransave = 0
        for k in range(0,24):
            i = (24*j) + k
            SouthTransave = SouthGlazingRadTrans[i] + SouthTransave
        aveDailySouthTrans.append(SouthTransave/24)
        
def running_mean_outdoor_temperature(temp_array, alpha=0.8): #this code is taken from pythermalcomfort library

    for i in range(0,365):
        if i < 6:
            temp_array7 = temp_array[0:i+1]
        else:
            temp_array7 = temp_array[i-6:i+1]
        coeff = [alpha ** ix for ix, x in enumerate(temp_array7)]
        t_rm = sum([a * b for a, b in zip(coeff, temp_array7)]) / sum(coeff)
        runSevenDay.append(t_rm)


def running_mean_south_transmitted(south_trans_array, alpha=0.8): #this code is taken from pythermalcomfort library

    for i in range(0,365):
        if i < 6:
            south_trans_array7 = south_trans_array[0:i+1]
        else:
            south_trans_array7 = south_trans_array[i-6:i+1]
        coeff = [alpha ** ix for ix, x in enumerate(south_trans_array7)]
        SSol_rm = sum([a * b for a, b in zip(coeff, south_trans_array7)]) / sum(coeff)
        runSevenDaySSolTrans.append(SSol_rm)
        
        
        




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
    
    
def get_weather_location(weather_file):
    csvfile = open(weather_file,'r')
    csvFileArray = []
    for row in csv.reader(csvfile, delimiter = ','):
        csvFileArray.append(row)
    return csvFileArray   
    
    

st.set_page_config(
    page_title="SolarShoeBox",
    #page_icon='/SolarShoeBoxSmall.jpg',
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
   
   
   values = st.slider(
    'Rotation from South',
    -90, 90, (0), key=0, step = 5)
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
col4.markdown('[Energyplus Weather](https://energyplus.net/weather)')



uploaded_file = col3.file_uploader('Upload Energyplus Weather File. File type must be .epw https://energyplus.net/weather', type= 'epw', help = WeatherFileUploaderHelp)
if uploaded_file is not None:

    #for location data from weather file



    reader = csv.reader(codecs.iterdecode(uploaded_file, 'utf-8'))
    row1 = next(reader)
    
    LSTM=-float(row1[8])*15
    
    longitude=-float(row1[7])
    
    latitude=float(row1[6])
    st.write('Longitude: ', str(longitude), 'and   Latitude: ',str(latitude))
    location=row1[1]
    State = row1[2]
    Country = row1[3]
   

    
    #For weather data from weather file
    
    ############################
    header=7
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
    aveDailyGHI = []
    
    aveDailySouthTrans = []
    runSevenDaySSolTrans = []
    runSevenDay =[]
    clLow80 = []
    clHigh80 = []
    clLow90 = []
    clHigh90 = []
    clMid =[]
    clLow80day = []
    clHigh80day = []
    Azimuth =[]
    Altitude = []
    Day = []
    Hour = []
    AltiAzmi(LSTM, latitude, longitude, x)
    Ave_Daily_AirTemp()
    Ave_Daily_GHI()
    running_mean_outdoor_temperature(aveDailyTemp, alpha=0.8)
    adaptive_ashrae(runSevenDay)
    for i in range(0, x):
        j= math.floor(i/24.0)
        clLow80day.append(clLow80[j])
        clHigh80day.append(clHigh80[j])
    SouthGlazingRadTrans = []
    GlazingRadTrans(90, 0, x)
    Ave_Daily_SouthTrans()
    running_mean_south_transmitted(aveDailySouthTrans, alpha=0.8)
    minaveDailyTemp = min(aveDailyTemp)
    minaveDailyGHI = min(aveDailyGHI)
    
    AveDayNumber = 10
    AveMinAveDailyTemp = heapq.nsmallest(AveDayNumber, aveDailyTemp)
    mintempave = float(sum(AveMinAveDailyTemp)/AveDayNumber)
    
    AveMinAveDailyGHI = heapq.nsmallest(AveDayNumber, aveDailyGHI)
    minghiave = float(sum(AveMinAveDailyGHI)/AveDayNumber)
                    
    
    plotSimpleWeather()
    st.write('Minimum Average Daily Outdoor Temperature: ', str(round(minaveDailyTemp,1)), '°C')
    st.write('Minimum Average Daily Global Horizontal Radiation: ', str(round(minaveDailyGHI,0)), 'W/m2')
    st.write(str(AveDayNumber),' Day Average Minimum Average Daily Outdoor Temperature: ', str(round(mintempave,1)), '°C')
    st.write(str(AveDayNumber),' Day Average Minimum Average Daily Global Horizontal Radiation: ', str(round(minghiave,0)), 'W/m2')
    #st.button('run')
    #plotWeather()

