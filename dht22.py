import Adafruit_DHT as dht    # Importing Adafruit library for DHT22
from time import sleep           # Impoting sleep from time library to add delay
import time, datetime
from collections import namedtuple

DURATION = 20
end_time = time.time() + DURATION


# try:
#     while time.time() < end_time:                # Loop will run forever
#         humi, temp = dht.read_retry(dht.DHT22, 8)  # Reading humidity and temperature
#         print('Temp: {0:0.1f}*C  Humidity: {1:0.1f}%'.format(temp, humi)) 
#         sleep(3)
# # If keyboard Interrupt is pressed
# except KeyboardInterrupt:
#     pass  			# Go to next line


def get_dht22_data():
    """ gets data from the dht22 sensor every interval seconds"""

    data_point = namedtuple('datapoint', 'timestamp humidity temperature' )
    try:
        humi, temp = dht.read_retry(dht.DHT22, 8)  # Reading humidity and temperature
        # get current time
        dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = data_point(dt, humi, temp)
    # If keyboard Interrupt is pressed
    except KeyboardInterrupt:
        data = None  			# Go to next line
    return data


if __name__ == "__main__":
    print(get_dht22_data())