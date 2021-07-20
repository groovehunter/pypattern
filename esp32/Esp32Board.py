from time import sleep
from Panel import Panel
from Esp32Light import Esp32Light
from DisplayBase_uP import DisplayBase
from ucollections import OrderedDict
import uasyncio as asyncio

class Esp32Board(DisplayBase):
    def __init__(self):
        print("init board")
        led = {}
        for i in range(1, 17):
          led[i] = Esp32Light(i)
        self.led = led
        print("init led array: %s", sorted(led))

    def init(self):
        self.init_panels()
        self.init_panel_lights()
        # neu
        self.total_pattern_list()

    def init_panels(self):
        self.panels = OrderedDict(
        {
          't' : Panel(1),
          'r' : Panel(2),
          'b' : Panel(3),
          'l' : Panel(4),
        })

    def init_panel_lights(self):
        for i, panel in self.panels.items():
            panel.init_lights()


    def all_on(self):
        for i, panel in self.panels.items():
            panel.full()

    def test(self):
        print("test func")
        led = self.led
        sl = 2
        for t in range(20):
            for n in range(1, 16, 2):
                led[n].pin.on()
            for n in range(2, 16, 2):
                led[n].pin.off()
            sleep(sl)
            for n in range(2, 16, 2):
                print(n)
                led[n].pin.on()
            for n in range(1, 16, 2):
                print(n)
                led[n].pin.off()
            await asyncio.sleep(sl)
            print(".", end='')
        print

    def switch_all(self, i):
        led[i].value(not led[i].value())

    def test_pattern(self):
        while True:
          print("test_pattern: next state")
          self.pattern.next_state()
          self.enlighten()
          await asyncio.sleep(1)


    def enlighten(self):
        for i, panel in self.panels.items():
          #print(panel.pid)
          #print(panel)
          for i, light in panel.lights.items():
            led_nr = ((panel.pid-1) * 4) + (i +1)
            #val = self.pattern.lights[led_nr].state
#            print(i, led_nr, val, self.led[led_nr].pin)
            self.led[led_nr].pin.value(light.state)
