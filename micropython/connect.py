# solid LED:	connected
# slow blink:	connecting
# fast blink:	failure


import network as nw
import machine
import time
try:
    import picozero
except ImportError:
    picozero = None

from networks import networks

def connect():
    if picozero:
        picozero.pico_led.blink()
    
    wlan = nw.WLAN(nw.STA_IF)
    wlan.config(pm = 0xa11140)  # Disable power-save mode
    wlan.active(True)
    for network in networks:
        print(f'Trying SSID: {network.ssid}')
        wlan.connect(network.ssid, network.password)
        
        max_wait = 7
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print(f'Waiting for connection... ({wlan.status()})')
            time.sleep(1)

        # Handle connection error
        if wlan.status() != 3:
            continue
        else:
            ip = wlan.ifconfig()[0]
            print(f'Connected as {ip} ({wlan.status()})')
            
            if picozero:
                picozero.pico_led.on()
            
            return wlan, ip
    else:
        if picozero:
            picozero.pico_led.blink(on_time=0.1)
 
        raise RuntimeError('network connection failed')


if __name__ == '__main__':
    connect()
