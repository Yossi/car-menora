import mip
from requirements import requirements

try:
    import connect
    wlan, ip = connect.connect()

    for requirement in requirements:
        try:
            print(' '.join( ('Checking', requirement.name, '|', requirement.url.rpartition('/')[2], '...') ), end=' ')
            __import__(requirement.name)
            print('OK')
        except ImportError:
            print('not present')
            mip.install(requirement.url, target=requirement.target) # this often fails when running on actual board. prefer to get these via mpremote on desktop


    # import set_time
    # set_time.set_time()

except RuntimeError:
    # network fail
    pass # leaves the led fast blinking

    print('Trying access point mode:')
    import host
    ap, ip = host.host() # run as an ap host with no connection to the wider internet

print(f'Running server at {ip}:5000')
import RGBserver
RGBserver.app.run()
