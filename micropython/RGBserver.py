from microdot import Microdot, send_file
from microdot.websocket import with_websocket
from shiftregister import register as r
from menorah import menorah as m
import json

app = Microdot()

m.lights = [1] * 9
m.display_lights()

clients = set()

@app.route('/ws')
@with_websocket
async def websocket(request, ws):
    # Add client to the set
    clients.add(ws)
    try:
        while True:
            message = await ws.receive()
            print(f'WebSocket message received: {message}')
            data = json.loads(message)
            command = data.get('command')
            if command == 'go':
                bits = data.get('bits')
                r.load(bits)
                await broadcast(json.dumps({'status': 'success', 'message': f'Colors updated to:\n{bits}'}))
            elif command == 'load':
                await ws.send(json.dumps({'status': 'success', 'bits': r.bits, 'message': 'Loaded colors'}))
            elif command == 'waveLight':
                await wave(request, 'light')
            elif command == 'waveDark':
                await wave(request, 'dark')
            elif command == 'party':
                times = data.get('times', 1)
                times = int(times) if times != "" else 1
                await party(request, times)
            elif command == 'stack':
                await stack(request)
            elif command == 'inOut':
                await in_out(request)
            elif command == 'lights':
                night_ = data.get('night', 8)
                night_ = int(night_) if night_ != "" else 8
                await night(request, night_)
            # Optionally handle other commands
    except Exception as e:
        print(f'WebSocket closed: {e}')
    finally:
        clients.remove(ws)

async def broadcast(message):
    '''Send a message to all connected WebSocket clients.'''
    for client in clients:
        try:
            await client.send(message)
        except Exception:
            clients.remove(client)

@app.route('/')
def index(request):
    return send_file('index.html')

@app.route('/night/<int:n>')
async def night(request, n):
    print(f'night {n}')
    await broadcast(json.dumps({'status': 'info', 'message': f'Changing to {n} lights'}))
    m.night(n)
    await broadcast(json.dumps({'status': 'success', 'message': f'Showing {n} lights'}))

@app.route('/bits/<bits>')
async def set_bits(request, bits):
    print(bits)
    await broadcast(json.dumps({'status': 'info', 'message': f'Updating colors to:\n{bits}'}))
    r.load(bits)
    await broadcast(json.dumps({'status': 'success', 'message': f'Colors updated to:\n{bits}'}))

@app.route('/bits')
def get_bits(request):
    return r.bits

@app.route('/lights/wave/<dark>')
async def wave(request, dark):
    if dark != 'light':
        dark = 'dark'
    # dark = False if dark == 'light' else True
    print('wave')
    await broadcast(json.dumps({'status': 'info', 'message': 'Running smooth wave'}))
    await m.smooth_wave(dark)
    await broadcast(json.dumps({'status': 'success', 'message': 'Done smooth wave'}))

@app.route('/lights/party/<int:times>')
async def party(request, times=1):
    print('party')
    await broadcast(json.dumps({'status': 'info', 'message': 'Doing party'}))
    await m.party_time(times, broadcast=broadcast)
    await broadcast(json.dumps({'status': 'success', 'message': 'Done party'}))

@app.route('/lights/stack')
async def stack(request):
    print('stack')
    await broadcast(json.dumps({'status': 'info', 'message': 'Running stack'}))
    await m.stack()
    await broadcast(json.dumps({'status': 'success', 'message': 'Done stack'}))

@app.route('/lights/in_out')
async def in_out(request):
    print('in_out')
    await broadcast(json.dumps({'status': 'info', 'message': 'Running in out'}))
    await m.in_out()
    await broadcast(json.dumps({'status': 'success', 'message': 'Done in out'}))

if __name__ == '__main__':
    app.run()
