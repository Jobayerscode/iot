import requests

#reference values by who 2021 in ug/m3 annaul
#pm2.5=5, pm10=15, ozone=60, no2=10, so2=40, co=4000
#reference values by who 2021 in ug/m3 24h
#pm2.5=15, pm10=45, ozone=100, no2=25, so2=40, co=4000
#https://www.who.int/news-room/feature-stories/detail/what-are-the-who-air-quality-guidelines
#EPA guidelines
#https://uk-air.defra.gov.uk/air-pollution/daqi?view=more-info&pollutant=no2#pollutant
#https://www.airnow.gov/sites/default/files/2020-05/aqi-technical-assistance-document-sept2018.pdf

#used for logging
#import json 
#result = json.dumps(response.json(), indent=2)
#print(result)


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
        data['current']['air_quality']['gb-defra-index']
    )


#algo, open windows to check if air quality improves if not increase window opening depending on outside conditions

def getScoreWHO(carbon, nitrogen, ozone, sulphur, small, large):
    # 0=best air quality, 1=2hr limit, 3=not great
    status=3
    if (carbon < 4000 and sulphur < 10 and nitrogen < 10 and ozone < 60 and small < 5 and large < 10):
        status=0
    elif(nitrogen < 25 and ozone < 100 and small < 25 and large < 45):
        status=1

    return status

def carbonLimit(carbon):
    return carbon < 4000

#UK AQI
ozoneRange = [33, 66, 100, 120, 140, 160, 187, 213, 240]
nitrogenRange = [67, 134, 200, 267, 334, 400, 467, 534, 600]
sulphurRange = [88, 177, 266, 354, 443, 532, 710, 887, 1064]
pm2Range = [11, 23, 35, 41, 47, 53, 58, 64, 70]
pm10Range = [16, 33, 50, 58, 66, 75, 83, 91, 100]


def getAQIrange(value, range):
    if value < range[0]:
        return 1
    elif value < range[1]:
        return 2
    elif value < range[2]:
        return 3
    elif value < range[3]:
        return 4
    elif value < range[4]:
        return 5
    elif value < range[5]:
        return 6
    elif value < range[6]:
        return 7
    elif value < range[7]:
        return 8
    elif value < range[8]:
        return 9
    else:
        return 10

def getAQImax(ozone, nitrogen, sulphur, small, large, ozoneRange, nitrogenRange, sulphurRange, pm2Range, pm10Range):
    return max(getAQIrange(ozone,ozoneRange),
                getAQIrange(nitrogen, nitrogenRange),
                getAQIrange(sulphur, sulphurRange),
                getAQIrange(small, pm2Range),
                getAQIrange(large, pm10Range))

#rain = 6 default modarate rain 4mm to 8mm
#wind = 14 default sand and dust starts blowing at 14.5 km/h

#Evaluation of window
def openWindow(wind, rain, condition, humidityOutdoor, humidityIndoor, tempOutdoor, tempIndoor, aqiOutdoor, aqiIndoor):
    winMultplier = 100

    if aqiOutdoor > aqiIndoor:
        return winMultplier = 0

    if wind > 14:
        return winMultplier = 0

    if tempIndoor < 18:
        return winMultplier = 0

    if condition > 1200:
        winMultplier = 0
    elif condition > 1100:
        winMultplier = 20
    else
        if rain > 6:
           winMultplier = 5
        elif humidityIndoor < 50 and humidityOutdoor > humidityIndoor:
            winMultplier = 15
        else
            if tempIndoor > tempOutdoor:
                winMultplier = 100
            else
                winMultplier = 50
    

    return winMultplier
   



temp, wind, rain, humidity, condition, carbon, nitrogen, ozone, sulphur, small, large, aqiIndoor =  getOutDoorDetails()

openWindow(wind, rain, condition, humidityOutdoor, humidityIndoor, tempOutdoor, tempIndoor, aqiOutdoor, aqiIndoor)

#print(getScoreWHO(carbon, nitrogen, ozone, sulphur, small, large))

#print(getAQImax(ozone, nitrogen, sulphur, small, large, ozoneRange, nitrogenRange, sulphurRange, pm2Range, pm10Range))

