import curses
import datetime
import threading
import time


class Window:
    def __init__(self):
        self.screen = curses.initscr()
        self.init_window()
        self.template_win = curses.newwin(1, 22, 4, 2)
        self.prompt_win = curses.newwin(1, 22, 5, 2)
        self.timer_win = curses.newwin(2, 22, 2, 60)
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
            time.sleep(0.1)

    def update_time(self):
        elapsed_time = datetime.datetime.now() - self.start_time
        self.place_cursor()
        if self.current_prompt:
            prompt_seconds = self.current_prompt.get_elapsed_time().seconds
            char_seconds = self.current_prompt.get_current_character().get_elapsed_time().seconds
            self.timer_win.addstr(0, 0, str(prompt_seconds).zfill(2))
            self.timer_win.addstr(1, 0, str(char_seconds).zfill(2))
            self.timer_win.refresh()

    def init_window(self):
        self.screen.clear()
        self.screen.border(0)
        self.screen.addstr(2, 2, "pyDTT - Ben Friedland")
        self.screen.refresh()

    def place_cursor(self):
        return
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
            #prompt_y, prompt_x = 5, 20 - len(str(self.current_prompt))
            self.screen.nodelay(0)
            _oord = self.screen.getch()
            input_char = chr(_oord).upper()
            if input_char == self.current_prompt.get_current_character().character:
                input_chars.append(input_char)
                if not self.current_prompt.advance():
                    return
            else:
                curses.beep()
                curses.flash()
                self.current_prompt.get_current_character().error()

    def update_pointer(self):
        self.prompt_win.addstr(0, 0, " " * 20)
        self.prompt_win.addch(0, self.current_prompt.position, curses.ACS_UARROW, curses.A_ALTCHARSET)
        self.prompt_win.refresh()