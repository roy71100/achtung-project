from time import sleep
import serial
from consts import Move

CODE_DOCT = {"B": 1, "F": 2, "L": 3, "R": 4, "B_R": 5, "F_R": 6, "L_R": 7, "R_R": 8}
DELAY = 0.0
from pynput.keyboard import Key, Listener

PRESSED_DICT = {"B": 0, "F": 0, "L": 0, "R": 0}
ser = None


def initialize():
    global ser
    print("Opening serial port to arduino...")
    ser = serial.Serial('COM3', 9600, timeout=0.05)  # Establish the connection on a specific port
    print("Opened")
    print("Listening...")


def send_command(move):
    # return

    if move == Move.RIGHT and PRESSED_DICT["R"] == 0:
        PRESSED_DICT["R"] = 1
        ser.write(bytes([CODE_DOCT["R"]]))

    if move == Move.LEFT and PRESSED_DICT["L"] == 0:
        PRESSED_DICT["L"] = 1
        ser.write(bytes([CODE_DOCT["L"]]))

    if move == Move.FORWARD and PRESSED_DICT["F"] == 0:
        PRESSED_DICT["F"] = 1
        ser.write(bytes([CODE_DOCT["F"]]))

    if move == Move.BACKWARD and PRESSED_DICT["B"] == 0:
        PRESSED_DICT["B"] = 1
        ser.write(bytes([CODE_DOCT["B"]]))

    if move == Move.STOP and PRESSED_DICT["F"] == 1:
        PRESSED_DICT["F"] = 0
        ser.write(bytes([CODE_DOCT["F_R"]]))

    if move == Move.STOP and PRESSED_DICT["B"] == 1:
        PRESSED_DICT["B"] = 0
        ser.write(bytes([CODE_DOCT["B_R"]]))

    if move == Move.UNRIGHT and PRESSED_DICT["R"] == 1:
        PRESSED_DICT["R"] = 0
        ser.write(bytes([CODE_DOCT["R_R"]]))

    if move == Move.UNLEFT and PRESSED_DICT["L"] == 1:
        PRESSED_DICT["L"] = 0
        ser.write(bytes([CODE_DOCT["L_R"]]))
