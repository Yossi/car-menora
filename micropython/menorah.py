from picozero import LED
from math import exp
from time import sleep
import asyncio
import json
from shiftregister import register as r

pins = 7,8,9,10,11,12,13,14,15
leds = [LED(pin) for pin in pins]

class Menorah(object):
    def __init__(self):
        self.lights = [0,0,0,0,0,0,0,0,0]
        self._night = 8
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
        self._night = n
        if n > 4:
            n += 1
        on = [1] * n
        off = [0] * (9-n)
        self.lights = on + off
        self.lights[4] = 1
        # print(self.lights)
        self.display_lights()

    async def stack(self):
        await asyncio.sleep(0)
        for led in leds:
            led.off()
        for x in range(9):
            for y in range(9-x):
                leds[y].on()
                sleep(.1)
                leds[y].off()
            leds[9-x-1].on()
        sleep(.1)
        self.display_lights()

    async def stack2(self):
        await asyncio.sleep(0)
        bits = r.bits
        bits_list = [bits[i:i+3] for i in range(0, len(bits), 3)]

        for led in leds[:4]+leds[5:]:
            led.off()
        for night in range(self._night):
            b = ''.join(bits_list[0:(1+night+int(night >= 4))])
            if 1 + night + int(night >= 4) < len(bits_list):
                fill = bits_list[night + int(night >= 4)] * (8 - night - int(night >= 4))
            else:
                fill = ''
            r.load((b+fill)[:12]+bits_list[4]+(b+fill)[15:])

            for frame in range(9-1, night, -1):
                if frame == 4:
                    continue
                leds[frame].on()
                sleep(.1)
                leds[frame].off()

            if night < 4:
                leds[frame-1].on()
            else:
                leds[frame].on()
        r.load(bits)


    async def party_time(self, times=1, broadcast=None):
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

        direction = [(9,), (8,-1,-1)]

        await asyncio.sleep(0)

        for x in range(*direction[1]):
            wipe(x)

        for t in range(times):
            for x in range(*direction[t%2]):
                move(x)
            if broadcast:
                await broadcast(json.dumps({"status": "info", "message": f"Party cycle {t + 1} of {times}"}))

        for x in range(*direction[(times)%2]):
            wipe(x, on=True)

        self.display_lights()

        #for i in range(360*2):
        #    for n, led in enumerate(leds):
        #        led.brightness = 0.51 + 0.49 * cos(radians(i-n*20))
        #    sleep(0.01)

    async def smooth_wave(self, dark=False):
        await asyncio.sleep(0)
        for q in (1024,-1,-1), (1024+1,):
            for t in range(*q):
                for n, led in enumerate(leds):
                    x = t/1024-(2*n+9)/32
                    if dark=='dark':
                        led.brightness = 1-exp(-200*x*x)
                    else:
                        led.brightness = exp(-200*x*x)

        sleep(.5)
        self.display_lights()

    async def in_out(self):
        await asyncio.sleep(0)
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
