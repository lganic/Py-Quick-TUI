import curses
from typing import Union, Tuple

_curses_stdscr = None

class Window:

    def __init__(self, root: Union[Window, None] = None, name: str = '', fullscreen: bool = False, size: Tuple[float, float] = (1, 1), pos: Tuple[float, float] = (0, 0), ):

        self.root = root
        self.name = name
        self.fullscreen = fullscreen
        self.size = size
        self.pos = pos

        if root is not None and fullscreen:

            raise ValueError("Attempted to make a non root window fullscreen.")


        if not _curses_stdscr:
            # Curses still needs to be initialized in the terminal. Call it.
            _curses_stdscr = curses.initscr()

            # Lets also take this opportunity to do the normal curses setup
            curses.noecho()
            curses.cbreak()
            _curses_stdscr.keypad(True)

                        