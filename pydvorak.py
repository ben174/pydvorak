#!/usr/bin/env python

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
        window.do_prompt(prompt)


class Prompt:
    """ A line of text the user must type. Also holds the speed at which the user typed the text
    and any error data.
    """

    def __init__(self, line):
        self.characters = [PromptCharacter(l) for l in list(line)]
        self.position = 0
        self.start_time = None
        self.done = False
        self.characters[0].start()

    def advance(self):
        self.characters[self.position].finish()
        self.position += 1
        if self.position == len(self.characters):
            self.done = True
            return False
        self.characters[self.position].start()
        return True

    def get_current_character(self):
        return self.characters[self.position].character

    def get_done_characters(self):
        return "".join(self.get_line()[0:self.position])

    def start(self):
        self.start_time = datetime.datetime.now()

    def finish(self):
        self.elapsed_time = None
        self.elapsed_time = datetime.datetime.now() - self.start_time

    def get_elapsed_time(self):
        return datetime.datetime.now() - self.start_time

    def get_line(self):
        return "".join([c.character for c in self.characters])

    def __str__(self):
        return self.get_line()

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

    def __str__(self):
        return self.character



class Window:
    def __init__(self):
        self.screen = curses.initscr()
        self.init_window()
        self.template_win = curses.newwin(1, 22, 4, 2)
        self.prompt_win = curses.newwin(1, 22, 5, 2)
        self.timer_win = curses.newwin(1, 22, 2, 60)
        self.timer_win.leaveok(True)
        self.current_prompt = None
        self.start_time = datetime.datetime.now()
        self.start_timer_thread()
        curses.noecho()
        self.screen.nodelay(True)

    def start_timer_thread(self):
        clock = threading.Thread(target=self.timer_thread_entry)
        clock.daemon = True
        clock.start()

    def timer_thread_entry(self):
        while 1:
            self.update_time()
            time.sleep(1)

    def update_time(self):
        elapsed_time = datetime.datetime.now() - self.start_time
        self.timer_win.addstr(0, 0, str(elapsed_time))
        self.timer_win.refresh()
        self.place_cursor()
        if self.current_prompt:
            #TODO: Current prompt timer
            pass

    def init_window(self):
        self.screen.clear()
        self.screen.border(0)
        self.screen.addstr(2, 2, "pyDTT - Ben Friedland")
        self.screen.refresh()

    def place_cursor(self):
        prompt_y, prompt_x = 5, 20 - self.current_prompt.position
        self.screen.move(prompt_y, prompt_x)

    def do_prompt(self, prompt):
        self.current_prompt = prompt
        self.current_prompt.start()
        self.update_time()
        self.template_win.addstr(0, 0, self.current_prompt.get_line(), curses.A_BOLD)
        self.template_win.refresh()
        input_chars = []
        while True:
            self.update_pointer()
            self.template_win.addstr(0, 0, self.current_prompt.get_done_characters())
            self.template_win.refresh()
            prompt_y, prompt_x = 5, 20 - len(str(self.current_prompt))
            self.screen.nodelay(0)
            _oord = self.screen.getch(prompt_y, prompt_x)
            input_char = chr(_oord).upper()
            if input_char == self.current_prompt.get_current_character():
                input_chars.append(input_char)
                if not self.current_prompt.advance():
                    return
            else:
                curses.beep()
                curses.flash()

    def update_pointer(self):
        self.prompt_win.addstr(0, 0, " " * 20)
        self.prompt_win.addch(0, self.current_prompt.position, curses.ACS_UARROW, curses.A_ALTCHARSET)
        self.prompt_win.refresh()


if __name__ == '__main__':
    main()
