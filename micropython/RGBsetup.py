from collections import namedtuple
import mip

Package = namedtuple('Package', 'name url path')
requirements = (
    Package('picozero', 'github:RaspberryPiFoundation/picozero/picozero/picozero.py', 'lib'),
    Package('microdot', 'github:miguelgrinberg/microdot/src/microdot/microdot.py', 'lib/microdot'),
    Package('microdot.websocket', 'github:miguelgrinberg/microdot/src/microdot/websocket.py', 'lib/microdot'),
    Package('microdot.websocket', 'github:miguelgrinberg/microdot/src/microdot/helpers.py', 'lib/microdot'),
    Package('microdot.websocket', 'github:miguelgrinberg/microdot/src/microdot/__init__.py', 'lib/microdot'),
)

try:
    import connect
    wlan, ip = connect.connect()
    
    for requirement in requirements:
        try:
            print('Checking ' + requirement.name + ' ...', end =" ")
            __import__(requirement.name)
            print('OK')
        except ImportError:
            print('not present')
            mip.install(requirement.url, target=requirement.path)
    
    #import set_time
    #set_time.set_time()
    
except RuntimeError:
    # network fail
    pass # leaves the led fast blinking
    
    print('Trying access point mode:') 
    import host
    ap, ip = host.host() # run as an ap host with no connection to the wider internet

'''
#######
import machine, time
Time = namedtuple('Time', 'year month day hour minute second dow doy')
def task(timer):
    print('woop')
    current_time = Time(*time.localtime())
    if current_time.hour == 2 and current_time.minute == 12:
        timer.deinit()

timer = machine.Timer()
timer.init(period=1000, mode=machine.Timer.PERIODIC, callback=task)
#######
'''
print(f'Running server at {ip}:5000')
import RGBserver
RGBserver.app.run()
