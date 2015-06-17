import curses
import datetime
import threading
import time
from string import ascii_uppercase


class Window:
    """ Contains all the view information for this application.

    """
    def __init__(self):
        self.screen = curses.initscr()
        self.init_window()
        self.error_win = curses.newwin(1, 22, 3, 2)
        self.template_win = curses.newwin(1, 22, 4, 2)
        self.prompt_win = curses.newwin(1, 22, 5, 2)
        self.timer_win = curses.newwin(2, 22, 2, 60)
        self.current_prompt = None
        self.start_time = datetime.datetime.now()
        self.start_timer_thread()
        curses.noecho()
        self.screen.nodelay(True)

    def start_timer_thread(self):
        """ Starts a new thread to update the timers.
        """
        clock = threading.Thread(target=self.timer_thread_entry)
        clock.daemon = True
        clock.start()

    def timer_thread_entry(self):
        while 1:
            self.update_time()
            time.sleep(0.1)

    def update_time(self):
        if self.current_prompt and not self.current_prompt.done:
            prompt_seconds = self.current_prompt.get_elapsed_time().seconds
            char_seconds = self.current_prompt.get_current_character().get_elapsed_time().seconds
            self.timer_win.addstr(0, 0, str(prompt_seconds).zfill(2))
            self.timer_win.addstr(1, 0, str(char_seconds).zfill(2))
            self.timer_win.refresh()
            self.place_cursor()

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
        # draw unfinished letters
        self.template_win.addstr(0, 0, self.current_prompt.get_line(), curses.A_BOLD)
        self.template_win.refresh()
        input_chars = []
        while True:
            self.update_pointer()
            # draw error line
            self.error_win.addstr(0, 0, " " * 20)
            for i, c in enumerate(self.current_prompt.characters):
                if c.error_count:
                    self.error_win.addch(0, i, curses.ACS_BULLET, curses.A_ALTCHARSET)
            self.error_win.refresh()
            # draw finished letters
            self.template_win.addstr(0, 0, self.current_prompt.get_done_characters())
            self.template_win.refresh()
            prompt_y, prompt_x = 5, 20 - len(str(self.current_prompt))
            self.screen.nodelay(0)
            _oord = self.screen.getch(prompt_y, prompt_x)
            input_char = chr(_oord).upper()
            if input_char == self.current_prompt.get_current_character().character:
                input_chars.append(input_char)
                if not self.current_prompt.advance():
                    return
            elif input_char in ascii_uppercase or input_char == ' ':
                curses.beep()
                curses.flash()
                self.current_prompt.get_current_character().error()
            else:
                # unrecognized character
                pass

    def update_pointer(self):
        self.prompt_win.addstr(0, 0, " " * 20)
        self.prompt_win.addch(0, self.current_prompt.position, curses.ACS_UARROW, curses.A_ALTCHARSET)
        self.prompt_win.refresh()
