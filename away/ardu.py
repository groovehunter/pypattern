

import pyfirmata
import time

led_pin = 9
board = pyfirmata.Arduino("/dev/ttyUSB0")
print("Code is running")

while True:
    board.digital[led_pin].write(0)
#    board.pass_time(3)
    time.sleep(1)
    board.digital[led_pin].write(1)
#    board.pass_time(3)
    time.sleep(1)
