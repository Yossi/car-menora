from shiftregister import register as r
from microdot import Microdot, send_file
from menorah import menorah as m
m.lights = [1] * 9
m.display_lights()

app = Microdot()

@app.route('/')
def index(request):
    return send_file('html.html')

@app.route('/night/<int:n>')
def night(request, n):
    print(f'night {n}')
    m.night(n)

@app.route('/bits/<bits>')
def bits(request, bits):
    print(bits)
    r.load(bits)    

@app.route('lights/wave/light')
def wave(request):
    m.smooth_wave()
    
@app.route('lights/wave/dark')
def wave(request):
    m.smooth_wave(dark=True)
    
@app.route('lights/party/<int:times>')
def wave(request, times=1):
    m.party_time(times)

@app.route('lights/stack')
def stack(request):
    m.stack()

@app.route('lights/in_out')
def in_out(request):
    m.in_out()

if __name__ == '__main__':
    app.run()