import Adafruit_DHT as dht    # Importing Adafruit library for DHT22
from time import sleep           # Impoting sleep from time library to add delay
import time
from datetime import datetime
import os
from dht22 import get_dht22_data

LOG_FILE = "./sensor-data/dht22_{}.log".format(datetime.now().strftime('%Y-%m-%d'))

#  log all data to a file

def log_data(interval):    
    # create file if not exist and write headers
    if not os.path.isfile(LOG_FILE):
        logfile = open(LOG_FILE, 'w+') 
        file_headers = "Timestamp,Humidity,Temperature\n"
        logfile.write(file_headers)
        logfile.close()

    # open file for normal appending
    logfile = open(LOG_FILE, 'a')

    while True:
        # read data
        data = get_dht22_data()
        # convert data to csv string
        csv_string = '{timestamp},{humidity},{temperature}\n'.format(**data._asdict())
        try:    
            # save data in file, add headers if file is empty  
            logfile.write(csv_string)
            sleep(interval)
        except KeyboardInterrupt:
            logfile.close()



# every x intervals, copy logged data in file to usb folder if usb is in drive




if __name__ == "__main__":
    log_data(3)