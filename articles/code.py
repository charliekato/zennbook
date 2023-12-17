import board
import digitalio
import usb_hid
# import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode


def keyin(keyNo):
    if keyNo == 14:
        kbd.send(Keycode.NINE)
    if keyNo == 13:
        kbd.send(Keycode.EIGHT)
    if keyNo == 12:
        kbd.send(Keycode.SEVEN)
    if keyNo == 11:
        kbd.send(Keycode.SIX)
    if keyNo == 10:
        kbd.send(Keycode.FIVE)
    if keyNo == 9:
        kbd.send(Keycode.FOUR)
    if keyNo == 8:
        kbd.send(Keycode.THREE)
    if keyNo == 7:
        kbd.send(Keycode.TWO)
    if keyNo == 6:
        kbd.send(Keycode.ONE)
    if keyNo == 5:
        kbd.send(Keycode.KEYPAD_MINUS)
    if keyNo == 4:
        kbd.send(Keycode.KEYPAD_PLUS)
    if keyNo == 3:
        kbd.send(Keycode.ZERO)
    if keyNo == 2:
        kbd.send(Keycode.ENTER)
    if keyNo == 1:
        kbd.send(Keycode.FORWARD_SLASH)
    if keyNo == 0:
        kbd.send(Keycode.KEYPAD_ASTERISK)

def gp_output(value1, value2, value3):
    swout1.value = value1
    swout2.value = value2
    swout3.value = value3
#
# swout1, swout2, swout3
def rotate_output(ctn):
    ctn = increment_counter(ctn)
    if ctn == 0:
        gp_output(False, True, True)
    if ctn == 10:
        gp_output(True, False, True)
    if ctn == 20:
        gp_output(True, True, False)
    return ctn

def increment_counter(counter):
    counter += 1
    if counter == 30:
        counter = 0
    return counter


def get_active_column(switch):
    if switch < 10:
        return 2
    if switch < 20:
        return 1
    return 0
'''
def get_row_value(sw5, sw4, sw3, sw2, sw1):
    rowValue = (sw5.value == 0) * 16
    rowValue = rowValue + (sw4.value == 0) * 8
    rowValue = rowValue + (sw3.value == 0) * 4
    rowValue = rowValue + (sw2.value == 0) * 2
    rowValue = rowValue + (sw1.value == 0)
    return rowValue
'''

def get_row_value(sw5, sw4, sw3, sw2, sw1):
    if sw5.value == 0:
        return 5
    if sw4.value == 0:
        return 4
    if sw3.value == 0:
        return 3
    if sw2.value == 0:
        return 2
    if sw1.value == 0:
        return 1
    return 0

counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
'''
def myLog(rowValue):
    if rowValue == 1:
        return 0
    if rowValue == 2:
        return 1
    if rowValue == 4:
        return 2
    if rowValue == 8:
        return 3
    if rowValue == 16:
        return 4
    return 0

def decode_key(rowValue, column):
    if rowValue == 0:
        for keyNo in range(column, 15, 3):
            counter[keyNo] = 0
    else:
        row = myLog(rowValue)
        keyNo = row * 3 + column
        if counter[keyNo] < 4:
            counter[keyNo] += 1
        if counter[keyNo] == 3:
            keyin(keyNo)
'''
CHATTERING_PREVENT_NUM=100
def decode_key(rowValue, column):
    if rowValue == 0:
        for keyNo in range(column, 15, 3):
            counter[keyNo] = 0
    else :
        keyNo = (rowValue - 1) * 3 + column
        if counter[keyNo] <= CHATTERING_PREVENT_NUM + 1:
            counter[keyNo] += 1
        if counter[keyNo] == CHATTERING_PREVENT_NUM:
            keyin(keyNo)

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

swout1 = define_output_pin(board.GP2)
swout2 = define_output_pin(board.GP1)
swout3 = define_output_pin(board.GP0)
#
# swout1, swout2, swout3
gp_output(False, True, True)
#
loopCounter = 0
#
while True:
    loopCounter = rotate_output(loopCounter)
    activeColumn = get_active_column(loopCounter)
    rowValue = get_row_value(sw5, sw4, sw3, sw2, sw1)
    decode_key(rowValue, activeColumn)


#
