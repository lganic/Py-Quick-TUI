import curses
from typing import Union, Tuple
from .animations import overflow_text_animation
from .table_chars import get_connected_char, get_wall_char, DetailMode

_curses_stdscr = None

class Window:

    def __init__(self, root: Union["Window", None] = None, name: str = '', fullscreen: bool = False, size: Tuple[float, float] = (1, 1), pos: Tuple[float, float] = (0, 0), detail: DetailMode = DetailMode.BASIC):

        global _curses_stdscr

        self.root = root
        self.name = name
        self.fullscreen = fullscreen
        self.size = size
        self.pos = pos

        self.detail = detail

        self._owns_curses = root is None

        if root is not None and fullscreen:

            raise ValueError("Attempted to make a non root window fullscreen.")

        if not _curses_stdscr:
            # Curses still needs to be initialized in the terminal. Call it.
            _curses_stdscr = curses.initscr()

            # Lets also take this opportunity to do the normal curses setup
            curses.noecho()
            curses.cbreak()
            _curses_stdscr.keypad(True)

        if root is None:
            self.root = _curses_stdscr
        else:
            self.root = root

        # Create the actual curses window.
        if fullscreen:
            
            self._win = _curses_stdscr

        elif root is None:
            self._win = curses.newwin(
                *(self.get_framed_size()[::-1]), # Flip coordinates, cause curses is backwards.
                *(self.get_framed_position()[::-1]), # Flip coordinates, cause curses is backwards.
            )

        else:
            self._win = root._win.derwin(
                *(self.get_framed_size()[::-1]), # Flip coordinates, cause curses is backwards.
                *(self.get_framed_position()[::-1]), # Flip coordinates, cause curses is backwards.
            )

    def close(self):
        global _curses_stdscr

        if self._win is None:
            return

        self._win = None

        if self._owns_curses and _curses_stdscr is not None:
            curses.nocbreak()
            _curses_stdscr.keypad(False)
            curses.echo()
            curses.endwin()

            _curses_stdscr = None

    def render(self, frame_count: int): # Frame count is used for animated elements.

        # Renders out just the box, and the elements.

        width, height = self._get_root_size()

        horz_wall_char = get_wall_char(False, detail = self.detail)
        vert_wall_char = get_wall_char(True,  detail = self.detail)

        # Top / bottom edges

        if width > 6:

            animated_string = overflow_text_animation(self.name, frame_count, width - 6)

            top_string = horz_wall_char + " " + animated_string + " " + horz_wall_char * (width - 5 - len(animated_string))

        else:
            top_string = horz_wall_char * (width - 2)

        self._win.addstr(0, 1, top_string)
        try:
            self._win.addstr(height - 1, 1, horz_wall_char * (width - 2)) # This throws error, due to stupid. But it still does the add.
        except curses.error:
            pass

        # Left / right edges
        for y in range(1, height - 1):
            try:
                self._win.addch(y, 0, vert_wall_char) # This throws error, due to stupid. But it still does the add.
            except curses.error:
                pass
            try:
                self._win.addch(y, width - 1, vert_wall_char) # This throws error, due to stupid. But it still does the add.
            except curses.error:
                pass

        # Corners
        self._win.addch(0, 0, get_connected_char(False, True, False, True, detail = self.detail))
        self._win.addch(0, width - 1, get_connected_char(False, True, True, False, detail = self.detail))

        try:
            # This throws error, due to stupid. But it still does the add.
            self._win.addch(height - 1, 0, get_connected_char(True, False, False, True, detail = self.detail))
        except curses.error:
            pass

        try:
            # This throws error, due to stupid. But it still does the add.
            self._win.addch(height - 1, width - 1, get_connected_char(True, False, True, False, detail = self.detail))
        except curses.error:
            pass

        self._win.refresh()

        

    def get_framed_position(self):

        root_size = self._get_root_size()

        return (
            int(root_size[0] * self.pos[0]),
            int(root_size[1] * self.pos[1])
        )

    def get_framed_size(self):

        root_size = self._get_root_size()

        return (
            int(root_size[0] * self.size[0]),
            int(root_size[1] * self.size[1])
        )

    def _get_root_size(self):

        return self.root.getmaxyx()[::-1] # Flip output, since I want to standardize width, height return.