import network as nw

''' this module makes the pi pico w act as an AP (with no internet access, of course) '''

ssid = 'RGBMenorah'
password = 'chanukah'

def host():
    ap = nw.WLAN(nw.AP_IF)
    ap.config(essid=ssid, password=password) 
    ap.config(pm = 0xa11140)
    ap.active(True)

    ip = ap.ifconfig()[0]

    print('Access point active')
    print(ip)
    return ap, ip

if __name__ == '__main__':
    host()
