import curses
import datetime
from string import ascii_uppercase


class Window:
    """ Contains all the view information for this application.

    """
    def __init__(self, screen, mapper=None):
        self.screen = screen
        self.mapper = mapper
        self.init_window()
        self.error_win = curses.newwin(1, 22, 3, 2)
        self.template_win = curses.newwin(1, 22, 4, 2)
        self.prompt_win = curses.newwin(1, 22, 5, 2)
        self.timer_win = curses.newwin(2, 22, 2, 60)
        self.score_win = curses.newwin(10, 14, 6, 60)
        self.score_win.border(1)
        self.score_win.addstr(1, 2, "SCOREBOARD")
        self.score_win.addstr(2, 2, "----------")
        self.score_win.box()
        self.score_win.refresh()
        self.current_prompt = None
        self.start_time = datetime.datetime.now()
        curses.noecho()
        self.screen.nodelay(True)


    def update_time(self):
        if self.current_prompt and not self.current_prompt.done:
            prompt_seconds = self.current_prompt.get_elapsed_time().seconds
            char_seconds = self.current_prompt.get_current_character().get_elapsed_time().seconds
            self.timer_win.addstr(0, 0, str(prompt_seconds).zfill(2))
            self.timer_win.addstr(1, 0, str(char_seconds).zfill(2))
            self.timer_win.refresh()
            self.place_cursor()

    def update_scores(self, scorecard, pool):
        for i, letter in enumerate(pool.pool):
            score = scorecard[letter]
            if score.prompt_characters:
                score_line = '{}: {}'.format(letter, str(score.get_average_speed()/100000.0))
            else:
                score_line = '{}: ------'.format(letter)

            self.score_win.addstr(i+3, 2, score_line)
        self.score_win.box()
        self.score_win.refresh()


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
            if self.mapper:
                input_char = self.mapper.map_key(input_char)

            if input_char == self.current_prompt.get_current_character().character:
                input_chars.append(input_char)
                # emits the current character out to the game class for scoring
                yield self.current_prompt.get_current_character()
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
