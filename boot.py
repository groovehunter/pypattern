
ESSID = 'WLAN-MJ7YSQ'
PASS  = '46804770364629155360'


#import upip

def connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ESSID, PASS)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def installpip():
  upip.install('micropython-uasyncio')
  upip.install('micropython-pkg_resources')


connect()
#installpip()
