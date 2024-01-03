from pi import openWindow, getAQImax
from data import outData, simulatedData

#print(openWindow(wind=5, rain=4, condition=1150, humidityOutdoor=30, humidityIndoor=50, tempOutdoor=5, tempIndoor=20, aqiOutdoor=1, aqiIndoor=2))
#print(getAQImax(ozone, nitrogen, sulphur, small, large))

# Imports for MQTT
import time
import datetime
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# Set MQTT broker and topic
broker = "test.mosquitto.org"	# Broker 

pub_topic = "multi/window"      # send messages to this topic

############### MQTT section ##################

# when connecting to mqtt do this;
def on_connect(client, userdata, flags, rc):
	if rc==0:
		print("Connection established. Code: "+str(rc))
	else:
		print("Connection failed. Code: " + str(rc))
		
def on_publish(client, userdata, mid):
    print("Published: " + str(mid))
	
def on_disconnect(client, userdata, rc):
	if rc != 0:
		print ("Unexpected disonnection. Code: ", str(rc))
	else:
		print("Disconnected. Code: " + str(rc))
	
def on_log(client, userdata, level, buf):		# Message is in buf
    print("MQTT Log: " + str(buf))
	
# Connect functions for MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.on_log = on_log

# Connect to MQTT 
print("Attempting to connect to broker " + broker)
client.connect(broker)	# Broker address, port and keepalive (maximum period in seconds allowed between communications with the broker)
client.loop_start()

# Loop that publishes message
while True:
      for count, value in enumerate(simulatedData):
		# Here, call the correct function from the sensor section depending on sensor
            data_to_send = openWindow(value["wind"],
                                    value["rain"], 
                                    value["condition"], 
                                    value["humidityOutdoor"],
                                    value["humidityIndoor"],
                                    value["tempOutdoor"],
                                    value["tempIndoor"],
                                    value["aqiOutdoor"], 
                                    value["aqiIndoor"])
            client.publish(pub_topic, str(data_to_send))
            time.sleep(2.0)	# Set delay
			
