from trainer.getch import _Getch
from util import hilite

class Game:
    def __init__(self):
        self.getch = _Getch()
        self.current_line = "ABCD EFGH IJKL"
        self.done_line = ""

    def start(self):
        self.loop()

    def print_board(self):
        print self.current_line
        print self.done_line
        print

    def loop(self):
        for letter in self.current_line:
            while True:
                self.print_board()
                input_letter = self.getch()
                if input_letter.lower() == letter.lower():
                    self.done_line += letter
                    break
        print hilite("done", True, True)
