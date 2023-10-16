import urequests as requests
import time
import machine

tz_offset = -8 # PST

def set_time():
    # network must be up first
    r = requests.get('http://date.jsontest.com')
    mils = r.json()['milliseconds_since_epoch']
    r.close() # saw documentation says this must be done manually
    mils += tz_offset * 3600 * 1000 # timezone
    time_tuple = time.localtime(mils // 1000)
    time_tuple = time_tuple[0:3] + (0,) + time_tuple[3:6] + (0,)
    machine.RTC().datetime(time_tuple)
    
if __name__ == '__main__':
    set_time()