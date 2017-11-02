from enum import Enum
import os, sys
import queue

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
        self.fifo = open(self.pipe_path, 'w')
        self.input_queue = queue.Queue()
        self.current_input = None
        self.frame_num = 0

    # Set the state of a button to either pressed or released
    def press_button(self, button, state, frames):
        self.input_queue.put([state + " " + button + "\n", frames])

    # Set the state of the C or MAIN stick, X and Y coordinates are 0 - 1
    def set_stick(self, stick, x, y, frames):
        self.input_queue.put(["SET " + stick + " " + x + " " + y + "\n", frames])

    # Set the percentage of the trigger down, 0 = not pressed, 1 = pressed
    # fully, trigger buttons can also be activated as buttons
    def set_trigger(self, trigger, state, frames):
        self.input_queue.put(["SET " + trigger + " " + state + "\n", frames])

    def next_input(self, frame_diff):
        if frame_diff == 0:
            return

        if not self.current_input:
            if not self.input_queue.empty():
                self.current_input = self.input_queue.get()
                self.fifo.write(self.current_input[0])
                self.fifo.flush()
                #if self.current_input[1] == 0:
                    #self.current_input = None
                    #self.next_input()
                    #return

                if frame_diff <= self.current_input[1]:
                    self.current_input[1] -= frame_diff
                    if self.current_input[1] == 0:
                        self.current_input = None

                elif frame_diff > self.current_input[1]:
                    frame_diff =- self.current_input[1]
                    self.current_input = None
                    if frame_diff > 0:
                        self.next_input(frame_diff)

                #self.current_input[1] -= 1
                #if self.current_input[1] == 0:
                    #self.current_input = None
        else:
            if frame_diff <= self.current_input[1]:
                self.current_input[1] -= frame_diff
                if self.current_input[1] == 0:
                    self.current_input = None

            elif frame_diff > self.current_input[1]:
                frame_diff =- self.current_input[1]
                self.current_input = None
                if frame_diff > 0:
                    self.next_input(frame_diff)
