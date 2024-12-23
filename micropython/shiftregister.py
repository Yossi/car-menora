from picozero import DigitalOutputDevice

data_pin = DigitalOutputDevice(2)
clock_pin = DigitalOutputDevice(5)
latch_pin = DigitalOutputDevice(4)

class Register(object):
    def __init__(self):
        self.load('1' * 27)
        rainbow = '100100110010111011001101101'
        self.load(rainbow)

    def load(self, bits):
        self.bits = bits
        #put latch down to start data sending
        clock_pin.off()
        latch_pin.off()
        clock_pin.on()

        #load data in reverse order
        for bit in reversed(bits):
            clock_pin.off()
            data_pin.value = int(bit)
            clock_pin.on()

        #put latch up to store data on register
        clock_pin.off()
        latch_pin.on()
        clock_pin.on()

register = Register()
