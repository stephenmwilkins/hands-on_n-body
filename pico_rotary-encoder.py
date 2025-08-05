# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT

"""I2C rotary encoder NeoPixel color picker and brightness setting example."""

import board
from rainbowio import colorwheel

from adafruit_seesaw import digitalio, neopixel, rotaryio, seesaw
import busio

# Initialize I2C using default pins (GP5 = SCL, GP4 = SDA on Pico)
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
seesaw = seesaw.Seesaw(i2c, 0x36)

encoder = rotaryio.IncrementalEncoder(seesaw)
seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
switch = digitalio.DigitalIO(seesaw, 24)

pixel = neopixel.NeoPixel(seesaw, 6, 1)
pixel.brightness = 0.5

last_position = -1
color = 0  # start at red

while True:
    # negate the position to make clockwise rotation positive
    position = -encoder.position

    if position != last_position:
        print(position)

        if switch.value:
            # Change the LED color.
            if position > last_position:  # Advance forward through the colorwheel.
                color += 1
            else:
                color -= 1  # Advance backward through the colorwheel.
            color = (color + 256) % 256  # wrap around to 0-256
            pixel.fill(colorwheel(color))

        elif position > last_position:  # Increase the brightness.
            pixel.brightness = min(1.0, pixel.brightness + 0.1)
        else:  # Decrease the brightness.
            pixel.brightness = max(0, pixel.brightness - 0.1)

    last_position = position
