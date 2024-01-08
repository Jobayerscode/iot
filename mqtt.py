import time
import random
import threading
import paho.mqtt.client as mqtt
from pi import openWindow, getAQI
from data import outData, simulatedData

task_running = False # Variable to track the state of the task
task_thread = None

pub_topic = "multi/window"      # send messages to this topic
sub_topic = "device/window"     # get messages from this topic

# Mockup function for the task
def run_task(client, pub_topic, simulatedData):
    while task_running:
        print("Task is running...")
        index = random.randint(0, len(simulatedData) - 1)
        jindex = random.randint(0, len(outData) - 1)
        kindex = random.randint(0, len(outData) - 1)
        data_to_send = openWindow(simulatedData[index]["wind"],
                                    simulatedData[index]["rain"], 
                                    simulatedData[index]["condition"], 
                                    simulatedData[index]["humidityOutdoor"],
                                    simulatedData[index]["humidityIndoor"],
                                    simulatedData[index]["tempOutdoor"],
                                    simulatedData[index]["tempIndoor"],
                                    getAQI(ozone=outData[jindex]["ozone"],
                                            nitrogen=outData[jindex]["nitrogen"], 
                                            sulphur=outData[jindex]["sulphur"], 
                                            small=outData[jindex]["small"], 
                                            large=outData[jindex]["large"]),
                                    getAQI(ozone=outData[kindex]["ozone"],
                                            nitrogen=outData[kindex]["nitrogen"], 
                                            sulphur=outData[kindex]["sulphur"], 
                                            small=outData[kindex]["small"], 
                                            large=outData[kindex]["large"]))
        
        client.publish(pub_topic, data_to_send)
        print(f"Published data: {data_to_send} to {pub_topic}")
        time.sleep(5)

# Callback when the client connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribe to the topic you are interested in
    client.subscribe(sub_topic)

# Callback when a message is received from the MQTT broker
def on_message(client, userdata, msg):
    global task_running, task_thread

    incoming_message = msg.payload.decode()
    print(f"Received message: {incoming_message} on topic {msg.topic}")

    # Assuming the incoming message is either 'True' or 'False'
    if incoming_message.lower() == 'true':
        # Start the task if not already running
        if not task_running:
            print("Starting the task...")
            task_running = True
            # Create a new thread for the task
            task_thread = threading.Thread(target=run_task, args=(client, pub_topic, simulatedData))
            task_thread.start()
        else:
            print("Task is already running.")
    elif incoming_message.lower() == 'false':
        # Stop the task if it's running
        if task_running:
            print("Stopping the task...")
            task_running = False
            client.publish(pub_topic, "0")
            print(f"Published data: 0 to {pub_topic}")
            # Wait for the task thread to finish
            task_thread.join()
        else:
            print("Task is not running.")
    else:
        print("Invalid message format")

# Create an MQTT client instance
client = mqtt.Client()

# Set the callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker (replace 'broker_address' with the actual address of your MQTT broker)
client.connect("test.mosquitto.org", 1883, 60)

# Loop to maintain the connection and process incoming messages
client.loop_forever()