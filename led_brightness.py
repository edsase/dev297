import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

led_pin = 19
GPIO.setup(led_pin, GPIO.OUT)

p = GPIO.PWM(led_pin, 50)  # channel=led_pin frequency=50Hz
p.start(0)
try:
    while 1:
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass

finally:
    p.stop()
    GPIO.cleanup()


