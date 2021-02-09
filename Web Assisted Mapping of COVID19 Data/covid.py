import json
import folium
import requests
import mimetypes
import http.client
import pandas as pd
from folium.plugins import HeatMap
from pandas.io.json import json_normalize
import shutil


conn = http.client.HTTPSConnection("api.covid19api.com")
payload = ''
headers ={}
conn.request("GET","/summary",payload,headers)
res=conn.getresponse()
data=res.read().decode('UTF-8')

covid1 = json.loads(data)

pd.json_normalize(covid1['Countries'],sep = ",")

df = pd.DataFrame(covid1['Countries'])

covid2 = df.drop(columns=['CountryCode','Slug','Date','Premium'],axis = 1)

m = folium.Map(tiles="Stamen Terrain",mini_zoom = 1.5)

m.save('default_map.html')
shutil.copy('default_map.html', 'templates')

url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
country_shapes = f'{url}/world-countries.json'

folium.Choropleth(
    geo_data = country_shapes,
    min_zoom = 2,
    name = 'Covid-19',
    data = covid2,
    columns=['Country','TotalConfirmed'],
    key_on = 'feature.properties.name',
    fill_color = 'OrRd',
    nan_fill_color= 'black',
    legend_name = 'Total Confirmed Covid Cases',
).add_to(m)

m.save('geodata_map.html')
shutil.copy('geodata_map.html', 'templates')

covid2.update(covid2['TotalConfirmed'].map('Total Confirmed:{}'.format))
covid2.update(covid2['TotalRecovered'].map('Total Recovered:{}'.format))

coordinates = pd.read_csv('https://raw.githubusercontent.com/VinitaSilaparasetty/covid-map/master/country-coordinates-world.csv')
covid_final = pd.merge(covid2,coordinates,on='Country')

def plotDot(point):
    folium.CircleMarker(location=[point.latitude,point.longitude],
    radius = 5,
    weight =2,
    popup = [point.Country,point.TotalConfirmed,point.TotalRecovered],
    fil_color = '#000000').add_to(m)

covid_final.apply(plotDot,axis = 1)
m.fit_bounds(m.get_bounds())

m.save('marker_map.html')
shutil.copy('marker_map.html', 'templates')

m1 = folium.Map(tiles='StamenToner',min_zoom = 2)
deaths = covid_final['TotalDeaths'].astype(float)
lat = covid_final['latitude'].astype(float)
lon = covid_final['longitude'].astype(float)
m1.add_child(HeatMap(zip(lat,lon,deaths),radius=0))

covid_final.update(covid_final['Country'].map('Country:{}'.format))
covid_final.update(covid_final['TotalDeaths'].map('Total Deaths:{}'.format))

def plotDot(point):
    folium.CircleMarker(location= [point.latitude,point.longitude],
    radius = 5,
    weight =2,
    popup=[point.Country,point.TotalDeaths],
    fill_color = '#000000').add_to(m1)

covid_final.apply(plotDot,axis = 1)
m1.fit_bounds(m1.get_bounds())

m1.save('heat_map.html')
shutil.copy('heat_map.html', 'templates')
        



    

