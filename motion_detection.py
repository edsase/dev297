import RPi.GPIO as GPIO
import io_settings
from led_blink import blink


# while True:
#     channel = GPIO.wait_for_edge(23, GPIO.RISING)
#     if channel is not None:
#         print('Motion detected')
#         blink(8)


def timestamp_motion_detection(val):
    from datetime import datetime
    from collections import namedtuple

    data = namedtuple('data', 'timestamp value')

    # current datetime
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    data = data(dt, 1)
    print(data)
    print('Motion detected') 
    blink(8)

    return data
    
    
if __name__ == "__main__":
    # add rising edge detection on channel 23
    GPIO.add_event_detect(23, GPIO.RISING, callback=timestamp_motion_detection)  
    while True:
        try:
            pass
            
        except KeyboardInterrupt:
            GPIO.cleanup()
        