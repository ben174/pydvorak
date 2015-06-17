import random
from prompt import Prompt
from scoring import ScoreCard
from window import Window


class Game:
    def __init__(self, screen):
        self.window = Window(screen)
        self.scorecard = ScoreCard()
        self.start()

    def start(self):
        while True:
            #pool = ascii_uppercase
            pool = 'EAINTO'
            prompt_line = " ".join(["".join([random.choice(pool) for r in range(4)]) for r in range(4)])
            prompt = Prompt(prompt_line)
            self.window.do_prompt(prompt)
            self.scorecard.consume_prompt(prompt)