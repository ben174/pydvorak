#!/usr/bin/env python

from string import ascii_uppercase
import random

from prompt import Prompt
from window import Window


def main():
    window = Window()
    while True:
        prompt_line = " ".join(["".join([random.choice(ascii_uppercase) for r in range(4)]) for r in range(4)])
        prompt = Prompt(prompt_line)
        window.do_prompt(prompt)


if __name__ == '__main__':
    main()
