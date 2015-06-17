import random
import threading
import time
from prompt import Prompt
from scoring import ScoreCard
from window import Window


class Game:
    def __init__(self, screen):
        self.scorecard = ScoreCard()
        self.window = Window(screen, self)
        self.start_timer_thread()
        self.start()

    def start(self):
        while True:
            #pool = ascii_uppercase
            pool = 'EAINTO'
            prompt_line = " ".join(["".join([random.choice(pool) for r in range(4)]) for r in range(4)])
            prompt = Prompt(prompt_line)
            self.window.do_prompt(prompt)
            self.scorecard.consume_prompt(prompt)

    def start_timer_thread(self):
        """ Starts a new thread to update the timers.
        """
        clock = threading.Thread(target=self.timer_thread_entry)
        clock.daemon = True
        clock.start()

    def timer_thread_entry(self):
        while 1:
            self.tick()
            time.sleep(0.1)

    def tick(self):
        """ Occurs every few milliseconds allowing the game to update timers and scoreboards. """
        self.window.update_time()
        self.window.update_scores()
