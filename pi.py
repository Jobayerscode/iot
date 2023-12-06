import requests
    
key=''
url='http://api.weatherapi.com/v1/current.json?'
location='Stockholm'
aqi='yes'

api_url = "{}key={}&q={}&aqi={}".format(url, key, location, aqi)
response = requests.get(api_url)

#used for logging
#import json 
#result = json.dumps(response.json(), indent=2)
#print(result)

#weather data
#print(data['current']['temp_c'])
#print(data['current']['wind_kph'])-
#print(data['current']['precip_mm'])
#print(data['current']['humidity'])

#air data
#print(data['current']['air_quality']['co'])
#print(data['current']['air_quality']['no2'])
#print(data['current']['air_quality']['o3'])
#print(data['current']['air_quality']['so2'])
#print(data['current']['air_quality']['pm2_5'])
#print(data['current']['air_quality']['pm10'])
#print(data['current']['air_quality']['us-epa-index'])

#default init
epa = 3 #default unhealty for sensitive groups
rain = 6 #default modarate rain 4mm to 8mm
wind = 14 #default sand and dust starts blowing at 14.5 km/h

data = response.json()

#variable general
temp = data['current']['temp_c']
wind = data['current']['wind_kph']
rain = data['current']['precip_mm']
humidity = data['current']['humidity']
condition = data['current']['condition']['code']

#variable air
carbon = data['current']['air_quality']['co']
nitrogen = data['current']['air_quality']['no2']
ozone = data['current']['air_quality']['o3']
sulphur = data['current']['air_quality']['so2']
small = data['current']['air_quality']['pm2_5']
large = data['current']['air_quality']['pm10']
epa = data['current']['air_quality']['us-epa-index']

#reference values by who 2021 in ug/m3 annaul
#pm2.5=5, pm10=15, ozone=60, no2=10, so2=40, co=4000
#reference values by who 2021 in ug/m3 24h
#pm2.5=15, pm10=45, ozone=100, no2=25, so2=40, co=4000
#https://www.who.int/news-room/feature-stories/detail/what-are-the-who-air-quality-guidelines

winMultplier = 100

#algo
