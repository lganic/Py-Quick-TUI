import curses
from typing import Union, Tuple, List
from .animations import overflow_text_animation
from .table_chars import get_connected_char, get_wall_char, DetailMode
from .content import Content, RenderSpace

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

        self.content: List[Content] = []

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

            new_width, new_height = self.get_framed_size()
            new_x, new_y = self.get_framed_position()

            new_width -= 2
            new_height -= 2
            new_x += 1
            new_y += 1

            self._win = root._win.derwin(
                new_height,
                new_width,
                new_y,
                new_x
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

        if self.root is not None and isinstance(self.root, Window):
            self.root.close() # Close parent window. Eventually we will close the root.

    def render(self, frame_count: int): # Frame count is used for animated elements.

        # Renders out just the box, and the elements.

        width, height = self.get_size()

        horz_wall_char = get_wall_char(False, detail = self.detail)
        vert_wall_char = get_wall_char(True,  detail = self.detail)

        # Top / bottom edges

        if width > 6:

            animated_string = overflow_text_animation(self.name, frame_count, width - 6)

            top_string = horz_wall_char + " " + animated_string + " " + horz_wall_char * (width - 5 - len(animated_string))

        else:
            top_string = horz_wall_char * (width - 2)

        self.put_text(1, 0, top_string)
        self.put_text(1, height - 1, horz_wall_char * (width - 2))

        # Left / right edges
        for y in range(1, height - 1):
            self.put_text(0, y, vert_wall_char)
            self.put_text(width - 1, y, vert_wall_char)

        # Corners
        self.put_text(0, 0, get_connected_char(False, True, False, True, detail = self.detail))
        self.put_text(width - 1, 0, get_connected_char(False, True, True, False, detail = self.detail))
        self.put_text(0, height - 1, get_connected_char(True, False, False, True, detail = self.detail))
        self.put_text(width - 1, height - 1, get_connected_char(True, False, True, False, detail = self.detail))

        available_render_space = RenderSpace(1, 1, width - 2, height - 2)

        for content_piece in self.content:
            rendered_size = content_piece.render(self, frame_count, available_render_space)

            available_render_space.y += rendered_size.height
            available_render_space.height -= rendered_size.height

            if not available_render_space.valid():
                break

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

    def get_size(self):

        return self._win.getmaxyx()[::-1] # Flip output, since I want to standardize width, height return.

    def _get_root_size(self):

        if isinstance(self.root, Window):
            return self.root._get_root_size()

        return self.root.getmaxyx()[::-1] # Flip output, since I want to standardize width, height return.
    
    def put_text(self, x: int, y: int, string: str):

        width, height = self._get_root_size()

        if x < 0:
            self.close()
            raise ValueError(f"X Coordinate Undersized: {x}")
        
        if y < 0:
            self.close()
            raise ValueError(f"Y Coordinate Undersized: {y}")
        
        if x > width - len(string):
            self.close()
            raise ValueError(f"String oversized for put. String length: {len(string)} X Pos: {x}")

        if y >= height:
            self.close()
            raise ValueError(f"Y Coordinate too large: {y}")

        try:
            if len(string) == 1:
                self._win.addch(y, x, string)
            else:
                self._win.addstr(y, x, string)
            
        except curses.error:
            pass # Ignore error, which might be due to the stupid plus 1 Y error.

    def add(self, new_content: Content):

        self.content.append(new_content)