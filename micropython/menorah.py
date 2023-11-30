from picozero import LED, Button
from math import sin, radians, cos, exp
from time import sleep
from machine import Timer

pins = 7,8,9,10,11,12,13,14,15
leds = [LED(pin) for pin in pins]

class Menorah(object):
    def __init__(self):
        self.lights = [0,0,0,0,0,0,0,0,0]
        for led in range(9):
            self.led_on_off(led, 1/9)
    
    def led_on_off(self, led, delay=1):
        leds[led].on()
        sleep(delay)
        leds[led].off()
    
    def display_lights(self):
        for n, led in enumerate(leds):
            led.brightness = self.lights[n]
    
    def night(self, n):
        if n > 4:
            n += 1
        on = [1] * n
        off = [0] * (9-n)
        self.lights = on + off
        self.lights[4] = 1
        print(self.lights)
        self.display_lights()

    def stack(self):
        for led in leds:
            led.off()
        for x in range(9):
            for y in range(9-x):
                leds[y].on()
                sleep(.1)
                leds[y].off()
            leds[9-x-1].on()

    def party_time(self, times=1):
        def move(x):
            leds[x].on()
            sleep(.1)
            leds[x].off()

        def wipe(x, on=False):
            if on:
                leds[x].on()
            else:
                leds[x].off()
            sleep(.1)
        
        direction = [(9,), (8,0,-1)]

        for x in range(*direction[1]):
            wipe(x)

        for t in range(times):
            for x in range(*direction[t%2]):
                move(x)                
            
        for x in range(*direction[(times)%2]):
            wipe(x, on=True)
            
            
        self.display_lights()
        
        #for i in range(360*2):
        #    for n, led in enumerate(leds):
        #        led.brightness = 0.51 + 0.49 * cos(radians(i-n*20))
        #    sleep(0.01)
        
    def smooth_wave(self, dark=False):
        for q in (1024,-1,-1), (1024+1,):
            for t in range(*q):
                for n, led in enumerate(leds):
                    x = t/1024-(2*n+9)/32
                    if dark:
                        led.brightness = 1-exp(-200*x*x)
                    else:
                        led.brightness = exp(-200*x*x)
        
        sleep(.5)
        self.display_lights()

    def in_out(self):
        for led in leds:
            led.off()
        leds[4].on()
        sleep(.1)
        
        for _ in range(3):
            for x in range(4):
                leds[3-x].on()
                leds[5+x].on()
                sleep(.1)
            
            for x in range(3,-1,-1):
                leds[3-x].off()
                leds[5+x].off()
                sleep(.1)

        self.display_lights()
        
        
menorah = Menorah()
