from pi import openWindow, getAQImax
from data import outData, simulatedData

#print(openWindow(wind=5, rain=4, condition=1150, humidityOutdoor=30, humidityIndoor=50, tempOutdoor=5, tempIndoor=20, aqiOutdoor=1, aqiIndoor=2))
#print(getAQImax(ozone, nitrogen, sulphur, small, large))

for count, value in enumerate(simulatedData):
      print(openWindow(value["wind"], value["rain"], value["condition"], value["humidityOutdoor"], value["humidityIndoor"], value["tempOutdoor"], value["tempIndoor"], value["aqiOutdoor"], value["aqiIndoor"] ))
