
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

i = 26
j = 3
t =0.6
panels = {} 
pins_LU = {
  1:19,
  2:26,
  3:13,
  4:6,
}

pins_LO = {
  1:11,
  2:10,
  3:5,
  4:9,
}
pins_RU = {
  1: 21,
  2: 20,
  3: 16,
  4: 12,
}
pins_RO = {
  1: 7,
  2: 8,
  3: 25,
  4: 24,
}
panels = {
  1: pins_LU,
  2: pins_LO,
  3: pins_RO,
  4: pins_RU,
}

pins = panels[4]
for i, pin in pins.items():
    GPIO.setup(pin, GPIO.OUT)

hi = GPIO.HIGH
lo = GPIO.LOW


def all(pins):
    while 1:
        print(pins),
        for p in range(1,5):
            GPIO.output(pins[p], hi)
        print("HIGH")
        for sl in range(4):
            print (sl)
            sleep(1)
        for p in range(1,5):
            GPIO.output(pins[p], lo)
        print("LOW")
        sleep(3)

all(pins)

#################
while 1:
    for p in range(1,5):
        print("growing", p)
        GPIO.output(pins[p], hi)
        sleep(1)
    # what else?

    print("blink")
    for s in range(5):
        for i, pin in pins.items():
            GPIO.output(pin, hi)
        sleep(0.2)
        for i, pin in pins.items():
            GPIO.output(pin, lo)
        sleep(0.2)
    print("blink finished")
    sleep(1)



while 1:
    for tf in range(1, 40):
        t = tf/33
        print("freq = 1 / ", t)
        GPIO.output(i, lo)
        GPIO.output(j, hi) 
        sleep(t)
        GPIO.output(i, hi) 
        GPIO.output(j, lo)
        sleep(t)
    for tf in range(40, 1):
        t = tf/33
        print("freq = 1 / ", t)
        GPIO.output(i, lo)
        GPIO.output(j, hi) 
        sleep(t)
        GPIO.output(i, hi) 
        GPIO.output(j, lo)
        sleep(t)

