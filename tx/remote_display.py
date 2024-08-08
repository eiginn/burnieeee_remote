## Dis stuff
import board
import displayio
from i2cdisplaybus import I2CDisplayBus
import terminalio
from adafruit_display_text import bitmap_label as label
from adafruit_displayio_sh1107 import SH1107, DISPLAY_OFFSET_ADAFRUIT_128x128_OLED_5297

try:
    i2c = board.STEMMA_I2C()

    displayio.release_displays()
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
except RuntimeError:
    # right now we don't use display
    pass
