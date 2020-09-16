
from time import sleep
import sys, os
if sys.platform == 'linux':
  sys.path.append(os.getcwd()+'/lib')

from Esp32Board import Esp32Board

class PDC:
    def __init__(self):
        print("init PDC")
        self.board = Esp32Board()
        #print(self.board.led)

pdc = PDC()

while True:
  print("running test")
  #print(pdc.board.led)
  pdc.board.init()
#  pdc.board.test()
  pdc.board.set_pattern('PairedLightsCycling')
  pdc.board.pattern.initial_state()
  pdc.board.test_pattern()
  #pdc.board.all_on()
#  print("next")
  sleep(5)
"""
"""
