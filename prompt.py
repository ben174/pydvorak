import datetime


class Timeable:
    """ Utility class which allows inheriting classes to be timed.  """
    def __init__(self):
        self.start_time = None
        self.stop_time = None

    def start(self):
        self.start_time = datetime.datetime.now()

    def finish(self):
        self.stop_time = datetime.datetime.now()

    def get_elapsed_time(self):
        return datetime.datetime.now() - self.start_time

    def get_timed_time(self):
        return self.stop_time - self.start_time


class Prompt(Timeable):
    """ A line of text the user must type.
    Also holds the speed at which the user typed the text and any error data.

    """
    def __init__(self, line):
        #super(Prompt, self).__init__()
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
        if self.done:
            return None
        return self.characters[self.position]

    def get_done_characters(self):
        return "".join(self.get_line()[0:self.position])

    def get_line(self):
        return "".join([c.character for c in self.characters])

    def __str__(self):
        return self.get_line()


class PromptCharacter(Timeable):
    """ A single character in a prompt.
    Holds the error count and the speed at which the letter was hit.

    """
    def __init__(self, char):
        #super(PromptCharacter, self).__init__()
        self.character = char
        self.start_time = None
        self.error_count = 0

    def error(self):
        self.error_count += 1

    def __str__(self):
        return self.character
