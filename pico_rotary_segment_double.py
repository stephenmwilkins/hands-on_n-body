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

# Initialise the first rotary encoder
seesaw1 = seesaw.Seesaw(i2c, 0x36)
encoder1 = rotaryio.IncrementalEncoder(seesaw1)
seesaw1.pin_mode(24, seesaw1.INPUT_PULLUP)
button1 = digitalio.DigitalIO(seesaw1, 24)
button1_held = False
pixel1 = neopixel.NeoPixel(seesaw1, 6, 1)
pixel1.brightness = 0.5
last_position1 = -1
color1 = 0  

# Initialise the second rotary encoder
seesaw2 = seesaw.Seesaw(i2c, 0x37)
encoder2 = rotaryio.IncrementalEncoder(seesaw2)
seesaw2.pin_mode(24, seesaw2.INPUT_PULLUP)
button2 = digitalio.DigitalIO(seesaw2, 24)
button2_held = False
pixel2 = neopixel.NeoPixel(seesaw2, 6, 1)
pixel2.brightness = 0.5
last_position2 = -1
color2 = 0  

# This creates a 7 segment 4 character display:
display1 = segments.Seg7x4(i2c, address=0x70)
display2 = segments.Seg7x4(i2c, address=0x71)

while True:

    # negate the position to make clockwise rotation positive
    position1 = -encoder1.position
   
    if position1 != last_position1:
        print(position1)
        
        display1.fill(0)
        display1.print(str(position1))
        
        # Change the LED color.
        if position1 > last_position1:  # Advance forward through the colorwheel.
            color1 += 1
        else:
            color1 -= 1  # Advance backward through the colorwheel.
        color1 = (color1 + 256) % 256  # wrap around to 0-256
        pixel1.fill(colorwheel(color1))

    # reset counter
    if not button1.value and not button1_held:
        button1_held = True
        encoder1.position = 0
        display1.fill(0)
        display1.print(0)
        color1 = 0  # wrap around to 0-256
        pixel1.fill(colorwheel(color1))

    if button1.value and button1_held:
        button1_held = False

    position2 = -encoder2.position
    if position2 != last_position2:
        print(position2)
        
        display2.fill(0)
        display2.print(str(position2))
        
        
        # Change the LED color.
        if position2 > last_position2:  # Advance forward through the colorwheel.
            color2 += 1
        else:
            color2 -= 1  # Advance backward through the colorwheel.
        color2 = (color2 + 256) % 256  # wrap around to 0-256
        pixel2.fill(colorwheel(color2))


    last_position1 = position1
    last_position2 = position2
    time.sleep(0.01)

