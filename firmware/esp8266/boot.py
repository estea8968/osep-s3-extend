#import esp
import uos, machine, time, network, gc
gc.collect()
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('estea-home', '89683086')
while not sta_if.isconnected():
    time.sleep(1)
    pass
print('network config:', sta_if.ifconfig())
