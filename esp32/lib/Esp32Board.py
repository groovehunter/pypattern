from time import sleep
from Panel import Panel
from Esp32Light import Esp32Light as Light
from DisplayBase_uP import DisplayBase
from ucollections import OrderedDict

class Esp32Board(DisplayBase):
    def __init__(self):
        print("init board")
        led = {}
        for i in range(1, 17):
          led[i] = Light(i)
          #sprint(led[i])
        self.led = led
        #print("OUTgoing pins: ", end='')
        print(sorted(led))

    def init(self):
        self.init_panels()
        self.init_panel_lights()

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
            sleep(sl)
            print(".", end='')
        print

    def switch(self, i):
        led[i].value(not led[i].value())

    def test_pattern(self):
        while True:
          self.pattern.next_state()
          self.enlighten()
          sleep(3)


    def enlighten(self):
        print("pattern: ", self.pattern.__class__)
        for i, panel in self.panels.items():
          print(panel)
          for i, light in panel.lights.items():
            led_nr = (panel.pid-1) * 4 + i +1
            val = self.pattern.lights[led_nr].state
            #print(led_nr, val)
            self.led[led_nr].pin.value(val)
