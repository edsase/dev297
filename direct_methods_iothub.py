# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import random
import time
import sys
import pickle

from led_blink import blink

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
import iothub_client
# pylint: disable=E0611
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

# import modules that connect to sensors on the device
from dht22 import get_dht22_data

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
fp_iot_hub_credentials = r"../credentials/iothub_credentials"
with open(fp_iot_hub_credentials, 'rb') as f:
    CONNECTION_STRING = pickle.load(f)

# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000

# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
HUMIDITY = 60
MSG_TXT = "{\"temperature\": %.2f,\"humidity\": %.2f}"

INTERVAL = 5

def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client

# Handle direct method calls from IoT Hub
def device_method_callback(method_name, payload, user_context):
    global INTERVAL
    print ( "\nMethod callback called with:\nmethodName = %s\npayload = %s" % (method_name, payload) )
    device_method_return_value = DeviceMethodReturnValue()
    if method_name == "SetTelemetryInterval":
        try:
            INTERVAL = int(payload)
            # call blink to let LED blink for number of seconds on payload
            blink(INTERVAL)
            # Build and send the acknowledgment.
            device_method_return_value.response = "{ \"Response\": \"Executed direct method %s\" }" % method_name
            device_method_return_value.status = 200
        except ValueError:
            # Build and send an error response.
            device_method_return_value.response = "{ \"Response\": \"Invalid parameter\" }"
            device_method_return_value.status = 400
    else:
        # Build and send an error response.
        device_method_return_value.response = "{ \"Response\": \"Direct method not defined: %s\" }" % method_name
        device_method_return_value.status = 404
    return device_method_return_value

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        # Set up the callback method for direct method calls from the hub.
        client.set_device_method_callback(
            device_method_callback, None)


        while True:
            # Build the message with simulated telemetry values.
            _, humidity, temperature = get_dht22_data()
            msg_txt_formatted = MSG_TXT % (temperature, humidity)
            message = IoTHubMessage(msg_txt_formatted)

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
            prop_map = message.properties()
            if temperature > 30:
              prop_map.add("temperatureAlert", "true")
            else:
              prop_map.add("temperatureAlert", "false")

            # Send the message.
            print( "Sending message: %s" % message.get_string() )
            client.send_event_async(message, send_confirmation_callback, None)
            time.sleep(INTERVAL)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #2 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()