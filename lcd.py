#!/usr/bin/env python3
from __future__ import annotations
import ipdb  # TODO: Remove this when done
import sys
import time
from rpi_lcd import LCD
from enum import Enum
from raspi import raspi as r


__GPIO_INIT = False
__GPIO_MODE = r.GPIO.BCM
__MAX_WIDTH = 10


class Pin(Enum):
	CONTRAST = 1
	REGISTER_SELECT = 2
	DATA_RW = 3
	ENABLE = 4
	DB0 = 5
	DB1 = 6
	DB2 = 7
	DB3 = 8
	DB4 = 9
	DB5 = 10
	DB6 = 11
	DB7 = 12
	DB8 = 13
	DB9 = 14

def init_hw(leds: [Led]) -> None:
    r.GPIO.setwarnings(False)
    r.GPIO.setmode(__GPIO_MODE)
    print(f'Set GPIO mode to: {__GPIO_MODE}')
    r.define_out_pins(list(map(lambda x: x.value, leds)))


def set(pin: Pin, mode: bool) -> None:
	if(mode):
	    r.pins_high(pin.value)
	else:
		r.pins_low(pin.value)


def clear_display():
	set(Pin.REGISTER_SELECT, False)
	set(Pin.DATA_RW, False)
	set(Pin.DB7, False)
	set(Pin.DB6, False)
	set(Pin.DB5, False)
	set(Pin.DB4, False)
	set(Pin.DB3, False)
	set(Pin.DB2, False)
	set(Pin.DB1, False)
	set(Pin.DB0, True)


def return_home():
	set(Pin.REGISTER_SELECT, False)
	set(Pin.DATA_RW, False)
	set(Pin.DB7, False)
	set(Pin.DB6, False)
	set(Pin.DB5, False)
	set(Pin.DB4, False)
	set(Pin.DB3, False)
	set(Pin.DB2, False)
	set(Pin.DB1, True)
	set(Pin.DB0, True)


def entry_mode_set(direction: bool, shift: bool):
	set(Pin.REGISTER_SELECT, False)
	set(Pin.DATA_RW, False)
	set(Pin.DB7, False)
	set(Pin.DB6, False)
	set(Pin.DB5, False)
	set(Pin.DB4, False)
	set(Pin.DB3, False)
	set(Pin.DB2, True)
	set(Pin.DB1, direction)
	set(Pin.DB0, shift)


def display_mode(all_on: bool, cursor_on: bool, cursor_pos_on: bool):
	set(Pin.REGISTER_SELECT, False)
	set(Pin.DATA_RW, False)
	set(Pin.DB7, False)
	set(Pin.DB6, False)
	set(Pin.DB5, False)
	set(Pin.DB4, False)
	set(Pin.DB3, True)
	set(Pin.DB2, all_on)
	set(Pin.DB1, cursor_on)
	set(Pin.DB0, cursor_pos_on)


def display_shift(: bool, cursor_on: bool, cursor_pos_on: bool):
	set(Pin.REGISTER_SELECT, False)
	set(Pin.DATA_RW, False)
	set(Pin.DB7, False)
	set(Pin.DB6, False)
	set(Pin.DB5, False)
	set(Pin.DB4, False)
	set(Pin.DB3, True)
	set(Pin.DB2, all_on)
	set(Pin.DB1, cursor_on)
	set(Pin.DB0, cursor_pos_on)


def hw_check(leds: [Led]) -> None:
    print('Hardware check:'.ljust(60, '-'))
    for led in leds:
        print(f'\tTesting LED {led} status...', end='')
        r.led_blink(led.value)
        print('Done!')
    print('Hardware check complete!'.ljust(60, '-'))


def main():
	if(len(sys.argv) == 1):
		print('Expected bytestring arg')
		sys.exit(-1)


	bytestring = sys.argv[1].rjust(__MAX_WIDTH, '0')
	if(len(bytestring) > __MAX_WIDTH):
		print('Bytestring can only be up to 8 bits!')
		sys.exit(-1)
	bytenum = int(f'0b{bytestring}', 2)
	bits = list(map(lambda x: int(x, 2), bytestring))

	print(f'Bytestring: {bytestring} ({bytenum})')
	print(bits)

	# Init all pins
	pins = []
	for i in range(1,15):
		pins.append(Pin(i))
	init_hw(pins)
	#hw_check(pins)  # Optional

	# Start pin read
	set(Pin.DATA_RW)
	set(Pin.ENABLE)
	
	# Enable pins according to bytestring
	for i, b in enumerate(bits):
		if(b == 1):
			# The +5 is the offset to the data bus lines
			pin = Pin(i + 5)
			print(f'Enabling pin: {pin}')
			set(pin)

	# Try some LCD stuff
	#print("Printing a message to the LCD")
	#lcd = LCD()
	#lcd.text('Hello world!')
	#time.sleep(3)
	#lcd.clear()


if __name__ == '__main__':
	main()
