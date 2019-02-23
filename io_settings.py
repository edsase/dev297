import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# set pin for LED
GPIO.setup(19, GPIO.OUT)

# set pin for pir data input
GPIO.setup(23, GPIO.IN)

# pin 8 is for DHT22 data readin


