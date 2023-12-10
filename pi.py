import requests

#used for logging
#import json 
#result = json.dumps(response.json(), indent=2)
#print(result)

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

#variable general
#temp = data['current']['temp_c']
#wind = data['current']['wind_kph']
#rain = data['current']['precip_mm']
#humidity = data['current']['humidity']
#condition = data['current']['condition']['code']

#variable air
#carbon = data['current']['air_quality']['co']
#nitrogen = data['current']['air_quality']['no2']
#ozone = data['current']['air_quality']['o3']
#sulphur = data['current']['air_quality']['so2']
#small = data['current']['air_quality']['pm2_5']
#large = data['current']['air_quality']['pm10']
#epa = data['current']['air_quality']['us-epa-index']

#reference values by who 2021 in ug/m3 annaul
#pm2.5=5, pm10=15, ozone=60, no2=10, so2=40, co=4000
#reference values by who 2021 in ug/m3 24h
#pm2.5=15, pm10=45, ozone=100, no2=25, so2=40, co=4000
#https://www.who.int/news-room/feature-stories/detail/what-are-the-who-air-quality-guidelines
#EPA guidelines
#https://www.airnow.gov/sites/default/files/2020-05/aqi-technical-assistance-document-sept2018.pdf


def getOutDoorDetails():
    key='4637ff343034453eb74214224230512'
    url='http://api.weatherapi.com/v1/current.json?'
    location='Stockholm'
    aqi='yes'

    api_url = "{}key={}&q={}&aqi={}".format(url, key, location, aqi)
    response = requests.get(api_url)
    data = response.json()
    return (
        data['current']['temp_c'],
        data['current']['wind_kph'],
        data['current']['precip_mm'],
        data['current']['humidity'],
        data['current']['condition']['code'],
        data['current']['air_quality']['co'],
        data['current']['air_quality']['no2'],
        data['current']['air_quality']['o3'],
        data['current']['air_quality']['so2'],
        data['current']['air_quality']['pm2_5'],
        data['current']['air_quality']['pm10'],
        data['current']['air_quality']['us-epa-index']
    )



epa = 3 #default unhealty for sensitive groups
rain = 6 #default modarate rain 4mm to 8mm
wind = 14 #default sand and dust starts blowing at 14.5 km/h


#algo, open windows to check if air quality improves if not increase window opening depending on outside conditions

def getEPA(carbon, nitrogen, ozone, sulphur, small, large):
    epa = 0
    
    return epa

def getScoreWHO(carbon, nitrogen, ozone, sulphur, small, large):
    # 0=best air quality, 1=2hr limit, 3=not great
    status=3
    if (carbon < 4000 and sulphur < 10 and nitrogen < 10 and ozone < 60 and small < 5 and large < 10):
        status=0
    elif(nitrogen < 25 and ozone < 100 and small < 25 and large < 45):
        status=1

    return status


def openWindow(temp, wind, rain, humidity, condition, epa):
    winMultplier = 100

    match epa:
        case 1:
            print( "zero")
        case 2:
            print( "1zero")
        case 3:
            print( "2zero")
        case 4:
            print( "3zero")
        case 5:
            print( "4zero")

    return winMultplier

#PM2.5 Sub-Index calculation
def getPM25(x):
    if x <= 30:
        return x * 50 / 30
    elif x <= 60:
        return 50 + (x - 30) * 50 / 30
    elif x <= 90:
        return 100 + (x - 60) * 100 / 30
    elif x <= 120:
        return 200 + (x - 90) * 100 / 30
    elif x <= 250:
        return 300 + (x - 120) * 100 / 130
    elif x > 250:
        return 400 + (x - 250) * 100 / 130
    else:
        return 0

#PM10 Sub-Index calculation
def getPM10(x):
    if x <= 50:
        return x
    elif x <= 100:
        return x
    elif x <= 250:
        return 100 + (x - 100) * 100 / 150
    elif x <= 350:
        return 200 + (x - 250)
    elif x <= 430:
        return 300 + (x - 350) * 100 / 80
    elif x > 430:
        return 400 + (x - 430) * 100 / 80
    else:
        return 0


#SO2 Sub-Index calculation
def getSO2(x):
    if x <= 40:
        return x * 50 / 40
    elif x <= 80:
        return 50 + (x - 40) * 50 / 40
    elif x <= 380:
        return 100 + (x - 80) * 100 / 300
    elif x <= 800:
        return 200 + (x - 380) * 100 / 420
    elif x <= 1600:
        return 300 + (x - 800) * 100 / 800
    elif x > 1600:
        return 400 + (x - 1600) * 100 / 800
    else:
        return 0

#NO2 Sub-Index calculation
def getNO2(x):
    if x <= 40:
        return x * 50 / 40
    elif x <= 80:
        return 50 + (x - 40) * 50 / 40
    elif x <= 180:
        return 100 + (x - 80) * 100 / 100
    elif x <= 280:
        return 200 + (x - 180) * 100 / 100
    elif x <= 400:
        return 300 + (x - 280) * 100 / 120
    elif x > 400:
        return 400 + (x - 400) * 100 / 120
    else:
        return 0

#CO Sub-Index calculation
def getCO(x):
    if x <= 1000:
        return x * 50 / 1
    elif x <= 2000:
        return 50 + (x - 1) * 50 / 1
    elif x <= 10000:
        return 100 + (x - 2) * 100 / 8
    elif x <= 17000:
        return 200 + (x - 10) * 100 / 7
    elif x <= 34000:
        return 300 + (x - 17) * 100 / 17
    elif x > 34000:
        return 400 + (x - 34) * 100 / 17
    else:
        return 0

#O3 Sub-Index calculation
def getO3(x):
    if x <= 50:
        return x * 50 / 50
    elif x <= 100:
        return 50 + (x - 50) * 50 / 50
    elif x <= 168:
        return 100 + (x - 100) * 100 / 68
    elif x <= 208:
        return 200 + (x - 168) * 100 / 40
    elif x <= 748:
        return 300 + (x - 208) * 100 / 539
    elif x > 748:
        return 400 + (x - 400) * 100 / 539
    else:
        return 0

def getAQI(x):
    if x <= 50:
        return 1
    elif x <= 100:
        return 2
    elif x <= 200:
        return 3
    elif x <= 300:
        return 4
    elif x <= 400:
        return 5
    elif x > 400:
        return 6



def findEPA(carbon, nitrogen, ozone, sulphur, small, large):
    epa = 6
    
    
    return epa




temp, wind, rain, humidity, condition, carbon, nitrogen, ozone, sulphur, small, large, epa =  getOutDoorDetails()

openWindow(temp, wind, rain, humidity, condition, epa)

print(getScoreWHO(carbon, nitrogen, ozone, sulphur, small, large))

