#!/usr/bin/env python

from os import system
import curses
from string import ascii_uppercase
import random
import threading
import time
import datetime


def main():
    window = Window()
    while True:
        prompt_line = " ".join(["".join([random.choice(ascii_uppercase) for r in range(4)]) for r in range(4)])
        prompt = Prompt(prompt_line)
        window.prompt(prompt)


class Prompt:
    """ A line of text the user must type. Also holds the speed at which the user typed the text
    and any error data.
    """

    def __init__(self, line):
        self.characters = [PromptCharacter(l) for l in list(line)]
        self.position = 0
        self.start_time = None
        self.done = False

    def advance(self):
        if self.position == len(self.characters):
            self.done = True
            return False
        self.position += 1
        self.characters[self.position].start()
        return True

    def current_character(self):
        return self.characters[self.position].character

    def get_line(self):
        return "".join([c.character for c in self.characters])

    def start(self):
        self.start_time = datetime.datetime.now()

    def finish(self):
        self.elapsed_time = None
        self.elapsed_time = datetime.datetime.now() - self.start_time

    def __unicode__(self):
        return "".join([c.character for c in self.characters])

class PromptCharacter:
    """ A single character in a prompt. Holds the error count and the speed at which the letter was hit.

    """
    def __init__(self, char):
        self.character = char
        self.start_time = None
        self.error_count = 0
        self.elapsed_time = None

    def start(self):
        self.start_time = datetime.datetime.now()

    def error(self):
        self.error_count += 1

    def finish(self):
        self.elapsed_time = datetime.datetime.now() - self.start_time

    def __unicode__(self):
        return self.character



class Window:
    def __init__(self):
        self.screen = curses.initscr()
        self.init_window()
        self.template_win = curses.newwin(1, 22, 4, 2)
        self.prompt_win = curses.newwin(1, 22, 5, 2)
        self.timer_win = curses.newwin(1, 22, 2, 60)
        self.timer_win.leaveok(True)
        self.start_timer_thread()
        self.current_prompt = None
        curses.noecho()

    def start_timer_thread(self):
        clock = threading.Thread(target=self.timer_thread_entry)
        clock.daemon = True
        clock.start()

    def timer_thread_entry(self):
        while 1:
            self.update_time()
            time.sleep(1)

    def update_time(self):
        elapsed_time = datetime.datetime.now() - self.prompt_start_time
        self.timer_win.addstr(0, 0, str(elapsed_time))
        self.timer_win.refresh()
        self.place_cursor()

    def init_window(self):
        self.screen.clear()
        self.screen.border(0)
        self.screen.addstr(2, 2, "pyDTT - Ben Friedland")
        self.screen.refresh()

    def place_cursor(self):
        prompt_y, prompt_x = 5, 20 - self.prompt_position
        self.screen.move(prompt_y, prompt_x)

    def prompt(self, prompt):
        self.current_prompt = prompt
        prompt.start()
        self.update_time()
        self.template_win.addstr(0, 0, prompt.get_line(), curses.A_BOLD)
        self.template_win.refresh()
        input_chars = []
        current_letter = prompt_chars.pop(0)
        while True:
            self.update_pointer()
            self.template_win.addstr(0, 0, str(prompt))
            self.template_win.refresh()
            prompt_y, prompt_x = 5, 20 - len(str(prompt))
            input_char = chr(self.screen.getch(prompt_y, prompt_x)).upper()
            if input_char == current_letter:
                if self.current_prompt.advance():
                    current_letter = prompt_chars.pop(0)
                else:
                    return
                input_chars.append(input_char)
            else:
                curses.beep()
                curses.flash()

    def update_pointer(self):
        self.prompt_win.addstr(0, 0, " " * 20)
        self.prompt_win.addch(0, self.current_prompt.position, curses.ACS_UARROW, curses.A_ALTCHARSET)
        self.prompt_win.refresh()


if __name__ == '__main__':
    main()
