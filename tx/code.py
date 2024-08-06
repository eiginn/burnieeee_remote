import board
import digitalio
import keypad
import neopixel
import adafruit_rfm69
import displayio

## Dis stuff
from i2cdisplaybus import I2CDisplayBus
import terminalio
from adafruit_display_text import bitmap_label as label
from adafruit_displayio_sh1107 import SH1107, DISPLAY_OFFSET_ADAFRUIT_128x128_OLED_5297


FLAME_ON_DURATION = 0.5

displayio.release_displays()

i2c = board.STEMMA_I2C()

display_bus = I2CDisplayBus(i2c, device_address=0x3D)

# Width, height and rotation for Monochrome 1.12" 128x128 OLED
WIDTH = 128
HEIGHT = 128
ROTATION = 90

# Border width
BORDER = 2

display = SH1107(
    display_bus,
    width=WIDTH,
    height=HEIGHT,
    display_offset=DISPLAY_OFFSET_ADAFRUIT_128x128_OLED_5297,
    rotation=ROTATION,
)

# Make the display context
splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000  # Black

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw some label text
name_text = "Burnieeeee\nFLAMES"
name_text_area = label.Label(terminalio.FONT, scale=2, text=name_text, color=0xFFFFFF, x=4, y=8)
splash.append(name_text_area)


## Radio parts
ENCKEY = bytearray("asdfghjklasdfghj", 'utf-8')
RADIO_FREQ_MHZ = 915.0
# Define Chip Select and Reset pins for the radio module.
CS = digitalio.DigitalInOut(board.RFM_CS)
RESET = digitalio.DigitalInOut(board.RFM_RST)

# Initialise RFM69 radio
rfm69 = adafruit_rfm69.RFM69(board.SPI(), CS, RESET, RADIO_FREQ_MHZ, encryption_key=ENCKEY)

## Keypad setup
keys = keypad.Keys((board.D13, board.D12, board.D11, board.D10), value_when_pressed=False, pull=True)
KEYMAP = {
    0: "UP",
    1: "LEFT",
    2: "DOWN",
    3: "RIGHT"
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
