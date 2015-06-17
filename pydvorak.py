#!/usr/bin/env python

import curses

from game import Game

def main():
    curses.wrapper(Game)


if __name__ == '__main__':
    main()
