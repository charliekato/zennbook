import board
import digitalio
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
keycode = [Keycode.KEYPAD_ASTERISK, Keycode.KEYPAD_FORWARD_SLASH, 0,
           Keycode.KEYPAD_ZERO, Keycode.KEYPAD_PLUS, Keycode.KEYPAD_MINUS,
           Keycode.KEYPAD_ONE, Keycode.KEYPAD_TWO, Keycode.KEYPAD_THREE,
           Keycode.KEYPAD_FOUR, Keycode.KEYPAD_FIVE, Keycode.KEYPAD_SIX,
           Keycode.KEYPAD_SEVEN, Keycode.KEYPAD_EIGHT, Keycode.KEYPAD_NINE,
           Keycode.ENTER, Keycode.BACKSPACE, Keycode.KEYPAD_NUMLOCK]
PADSHIFT = 2
NUMLOCK = 17
ENTER = 15
BACK = 16

def gp_output(value1, value2, value3):
    swout1.value = value1
    swout2.value = value2
    swout3.value = value3
#
# swout1, swout2, swout3
def rotate_output():
    global loopCounter
    increment_counter()
    if loopCounter == 0:
        gp_output(0, 1, 1)
    if loopCounter == 10:
        gp_output(1, 0, 1)
    if loopCounter == 20:
        gp_output(1, 1, 0)

def increment_counter():
    global loopCounter
    loopCounter += 1
    if loopCounter == 30:
        loopCounter = 0


def get_active_column(switch):
    if switch < 10:
        return 0
    if switch < 20:
        return 1
    return 2

def get_rowValue(sw5, sw4, sw3, sw2, sw1):
    rawValue = (sw5.value == 0) * 16 + \
            (sw4.value == 0) * 8 + \
            (sw3.value == 0) * 4 + \
            (sw2.value == 0) * 2 + \
            (sw1.value == 0)
    return rawValue

def get_keyNo(rowValue, column):
    if rowValue == 16:
        return 12 + column
    if rowValue == 8:
        return 9 + column
    if rowValue == 4:
        return 6 + column
    if rowValue == 2:
        return 3 + column
    if rowValue == 1:
        return column
    if rowValue == 17:
        return NUMLOCK
    if rowValue == 5:
        return BACK
    if rowValue == 3:
        return ENTER


counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

CHATTERING_PREVENT_NUM = 100
HALF_OF_CHATNUM = 50

def key_release(keyNo):
    if counter[keyNo] == CHATTERING_PREVENT_NUM:
        counter[keyNo] = HALF_OF_CHATNUM
    if counter[keyNo] >= 1:
        counter[keyNo] -= 1
    if counter[keyNo] == 1:
        kbd.release(keycode[keyNo])


def key_press(keyNo):
    if counter[keyNo] == 0:
        counter[keyNo] = HALF_OF_CHATNUM
    if counter[keyNo] <= CHATTERING_PREVENT_NUM:
        counter[keyNo] += 1
    if counter[keyNo] == CHATTERING_PREVENT_NUM:
        kbd.press(keycode[keyNo])


def decode_key(rowValue, column):
    if ((rowValue == 1) and (column == 2)) or (rowValue == 0):
        if column == 2:
            for keyNo in range(15, 18, 1):
                key_release(keyNo)
            for keyNo in range(5, 15, 3):
                key_release(keyNo)
        else:
            for keyNo in range(column, 15, 3):
                key_release(keyNo)
    else:
        keyNo = get_keyNo(rowValue, column)
        key_press(keyNo)

def define_input_pin(boardpin):
    inpin = digitalio.DigitalInOut(boardpin)
    inpin.direction = digitalio.Direction.INPUT
    inpin.pull = digitalio.Pull.UP
    return inpin

def define_output_pin(boardpin):
    outpin = digitalio.DigitalInOut(boardpin)
    outpin.switch_to_output(drive_mode=digitalio.DriveMode.OPEN_DRAIN)
    return outpin

#
kbd = Keyboard(usb_hid.devices)
sw5 = define_input_pin(board.GP28)
sw4 = define_input_pin(board.GP27)
sw3 = define_input_pin(board.GP26)
sw2 = define_input_pin(board.GP22)
sw1 = define_input_pin(board.GP21)

swout3 = define_output_pin(board.GP2)
swout2 = define_output_pin(board.GP1)
swout1 = define_output_pin(board.GP0)
#
# swout1, swout2, swout3
gp_output(0, 1, 1)
#
loopCounter = 0
#
while True:
    rotate_output()
    activeColumn = get_active_column(loopCounter)
    rowValue = get_rowValue(sw5, sw4, sw3, sw2, sw1)
    decode_key(rowValue, activeColumn)

#
