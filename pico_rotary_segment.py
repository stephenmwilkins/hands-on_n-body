# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT

"""I2C rotary encoder NeoPixel color picker and brightness setting example."""

import board
from rainbowio import colorwheel
from adafruit_ht16k33 import segments
from adafruit_seesaw import digitalio, neopixel, rotaryio, seesaw
import busio
import time

# Initialize I2C using default pins (GP5 = SCL, GP4 = SDA on Pico)
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
seesaw1 = seesaw.Seesaw(i2c, 0x36)

encoder1 = rotaryio.IncrementalEncoder(seesaw1)
seesaw1.pin_mode(24, seesaw1.INPUT_PULLUP)
switch1 = digitalio.DigitalIO(seesaw1, 24)

pixel1 = neopixel.NeoPixel(seesaw1, 6, 1)
pixel1.brightness = 0.5

last_position = -1
color = 0  # start at red

# This creates a 7 segment 4 character display:
display = segments.Seg7x4(i2c)


while True:

    

    # negate the position to make clockwise rotation positive
    position = -encoder1.position

    if position != last_position:
        print(position)
        
        display.fill(0)
        display.print(str(position))
        
        if switch1.value:
            # Change the LED color.
            if position > last_position:  # Advance forward through the colorwheel.
                color += 1
            else:
                color -= 1  # Advance backward through the colorwheel.
            color = (color + 256) % 256  # wrap around to 0-256
            pixel1.fill(colorwheel(color))


        elif position > last_position:  # Increase the brightness.
            pixel1.brightness = min(1.0, pixel1.brightness + 0.1)
        else:  # Decrease the brightness.
            pixel1.brightness = max(0, pixel1.brightness - 0.1)

    last_position = position
    time.sleep(0.01)

