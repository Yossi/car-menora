from shiftregister import register as r
from microdot import Microdot, send_file
from microdot.websocket import with_websocket
from menorah import menorah as m
import asyncio
from time import sleep

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
            print(f"WebSocket message received: {message}")
            # Optionally handle messages from the client
    except Exception as e:
        print(f"WebSocket closed: {e}")
    finally:
        clients.remove(ws)

async def broadcast(message):
    """Send a message to all connected WebSocket clients."""
    for client in clients:
        try:
            await client.send(message)
        except Exception:
            clients.remove(client)

@app.route('/')
def index(request):
    return send_file('html.html')

@app.route('/night/<int:n>')
def night(request, n):
    print(f'night {n}')
    asyncio.create_task(broadcast(f"Changing to {n} lights"))
    m.night(n)
    asyncio.create_task(broadcast(f"Showing {n} lights"))

@app.route('/bits/<bits>')
def bits(request, bits):
    print(bits)
    asyncio.create_task(broadcast(f"Updating colors to {bits}"))
    r.load(bits)
    asyncio.create_task(broadcast(f"Colors updated to {bits}"))

@app.route('/lights/wave/<dark>')
async def wave(request, dark):
    dark = False if dark == 'light' else True
    print('wave')

    asyncio.create_task(broadcast("Doing smooth wave"))
    await m.smooth_wave(dark)
    asyncio.create_task(broadcast("Smooth wave done"))

@app.route('lights/party/<int:times>')
async def wave(request, times=1):
    print('party')
    asyncio.create_task(broadcast("Doing party"))
    await m.party_time(times)
    asyncio.create_task(broadcast("Party done"))

@app.route('lights/stack')
async def stack(request):
    print('stack')
    asyncio.create_task(broadcast("Doing stack"))
    await m.stack()
    asyncio.create_task(broadcast("Stack done"))

@app.route('lights/in_out')
async def in_out(request):
    asyncio.create_task(broadcast("Doing in out"))
    await m.in_out()
    asyncio.create_task(broadcast("In out done"))

if __name__ == '__main__':
    app.run()