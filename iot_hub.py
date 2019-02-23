import pickle

from iothub_client import IoTHubClient, IoTHubTransportProvider, IoTHubMessage
import time



fp_iot_hub_credentials = r"../credentials/iothub_credentials"

with open(fp_iot_hub_credentials, 'rb') as f:
    # Azure IoT Hub
    CONNECTION_STRING = pickle.load(f)
    # URI = pickle.load(f)
    # KEY = pickle.load(f)
    # IOT_DEVICE_ID = pickle.load(f)
    # POLICY = pickle.load(f)
    
PROTOCOL = IoTHubTransportProvider.MQTT


def send_confirmation_callback(message, result, user_context):
    print("Confirmation received for message with result = %s" % (result))


if __name__ == '__main__':
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    message = IoTHubMessage("test message")
    client.send_event_async(message, send_confirmation_callback, None)
    print("Message transmitted to IoT Hub")

    while True:
        time.sleep(1)
