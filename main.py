from machine import UART, Pin
import socket
import time

TX = 17
RX = 16
BREAKPIN = 4

ARTNET_PORT = 6454
UNIVERSE = 0 # Auswahl ueber Nummer von Universum (0-15)
CHANNELS = 512

ARTNET_ID = b"Art-Net\0"
OPCODE_DMX = 0x5000

# 40 Hz = 25MS = 25000us => 512 Channels
FRAME_US = 30000

# DMX Buffer (Startcode + 512 Slots)
dmx_buffer = bytearray(1 + CHANNELS)
dmx_buffer[0] = 0x00

# UART dauerhaft initialisiert
uart = UART(2, baudrate=250_000, bits=8, parity=None, stop=2, tx=TX, rx=RX)

# TX Pin für Break/MAB (bleibt als Pin-Objekt vorhanden)
breakpin = Pin(BREAKPIN, Pin.OUT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", ARTNET_PORT))
sock.setblocking(False)

print("Art-Net → DMX Bridge aktiv – Universe", UNIVERSE)
 
def poll_artnet():
    try:
        data, _ = sock.recvfrom(530) 
    except OSError:
        return False

    if len(data) < 18 or data[:8] != ARTNET_ID:
        return False

    if (data[8] | (data[9] << 8)) != OPCODE_DMX:
        return False

    uni = data[14] | (data[15] << 8)
    if uni != UNIVERSE:
        return False

    length = (data[16] << 8) | data[17]
    if length <= 0:
        return False

    n = length if length < CHANNELS else CHANNELS
    
    dmx_buffer[1:1 + n] = data[18:18 + n]
    if n < CHANNELS:
        dmx_buffer[1 + n:] = b"\x00" * (CHANNELS - n)
    return True

def dmx_send_frame():
    breakpin.value(0) 
    time.sleep_us(110)
    breakpin.value(1)
    uart.write(dmx_buffer)

last_send = time.ticks_us()

while True:
    poll_artnet()
    now = time.ticks_us()
    if time.ticks_diff(now, last_send) >= FRAME_US:
        last_send = now
        dmx_send_frame()
    time.sleep_ms(0)
