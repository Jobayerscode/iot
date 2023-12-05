import requests
import json     

key='4637ff343034453eb74214224230512'
url='http://api.weatherapi.com/v1/current.json?'
location='Stockholm'
aqi='yes'

api_url = "{}key={}&q={}&aqi={}".format(url, key, location, aqi)
response = requests.get(api_url)

#used for logging
result = json.dumps(response.json(), indent=2)
print(result)

#weather data
#print(data['current']['temp_c'])
#print(data['current']['wind_kph'])
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

winMultplier = 100










