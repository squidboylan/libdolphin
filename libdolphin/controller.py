from enum import Enum
import os, sys

class Buttons(Enum):
    press = "PRESS"
    release = "RELEASE"

    A = "A"
    B = "B"
    X = "X"
    Y = "Y"
    Z = "Z"

    main_stick = "MAIN"
    c_stick = "C"
    L = "L"
    R = "R"

class Controller:
    def __init__(self, pipe_path):
        self.pipe_path = pipe_path
        self.fifo = os.open(self.pipe_path, 'w')

    # Set the state of a button to either pressed or released
    def press_button(self, button, state):
        self.fifo.write(state + " " + button)

    # Set the state of the C or MAIN stick, X and Y coordinates are 0 - 1
    def set_stick(self, stick, x, y):
        self.fifo.write("SET " + stick + " " + x + " " + y)

    # Set the percentage of the trigger down, 0 = not pressed, 1 = pressed
    # fully, trigger buttons can also be activated as buttons
    def set_trigger(self, trigger, state):
        self.fifo.write("SET " + trigger + " " + state)
