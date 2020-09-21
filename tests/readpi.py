
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

i = 21
GPIO.setup(i, GPIO.IN)

hi = GPIO.HIGH
lo = GPIO.LOW

while 1:
    val = GPIO.input(i)
    print("next", val)
    sleep(1)

