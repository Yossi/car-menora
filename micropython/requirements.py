from collections import namedtuple

Package = namedtuple('Package', 'name url target')
requirements = (
    Package('picozero', 'github:RaspberryPiFoundation/picozero/picozero/picozero.py', 'lib/picozero'),
    Package('picozero', 'github:RaspberryPiFoundation/picozero/picozero/__init__.py', 'lib/picozero'),
    Package('microdot', 'github:miguelgrinberg/microdot/src/microdot/microdot.py', 'lib/microdot'),
    Package('microdot.websocket', 'github:miguelgrinberg/microdot/src/microdot/websocket.py', 'lib/microdot'),
    Package('microdot.websocket', 'github:miguelgrinberg/microdot/src/microdot/helpers.py', 'lib/microdot'),
    Package('microdot.websocket', 'github:miguelgrinberg/microdot/src/microdot/__init__.py', 'lib/microdot'),
)
