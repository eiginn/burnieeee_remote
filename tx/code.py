import board
import digitalio
import keypad
import neopixel
import adafruit_rfm69
from remote_display import *


FLAME_ON_DURATION = 0.5


## Radio parts
ENCKEY = bytearray("asdfghjklasdfghj", 'utf-8')
RADIO_FREQ_MHZ = 915.0
# Define Chip Select and Reset pins for the radio module.
CS = digitalio.DigitalInOut(board.RFM_CS)
RESET = digitalio.DigitalInOut(board.RFM_RST)

# Initialise RFM69 radio
rfm69 = adafruit_rfm69.RFM69(board.SPI(), CS, RESET, RADIO_FREQ_MHZ, encryption_key=ENCKEY)

## Keypad setup
keys = keypad.Keys((board.D13, board.D12, board.D11, board.D10, board.D5), value_when_pressed=False, pull=True)
KEYMAP = {
    0: "UP",
    1: "LEFT",
    2: "DOWN",
    3: "RIGHT",
    4: "BIBBUTTON"
}

# Create an event to reuse, avoid frequent allocation
event = keypad.Event()

while True:
    # Check if we lost some events.
    if keys.events.overflowed:
        k.events.clear()  # Empty the event queue.
        k.reset()  # Forget any existing presses. Start over.

    if keys.events.get_into(event):
        if event.pressed:
            print(KEYMAP[event.key_number])
            # send string since int 0 in bytes breaks
            rfm69.send(bytes(f"{event.key_number}", "utf-8"))
