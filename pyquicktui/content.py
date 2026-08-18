from typing import TYPE_CHECKING
from .animations import overflow_text_animation

if TYPE_CHECKING:
    from .window import Window

class Content:

    def render(self, target_window: "Window", frame_count: int):

        raise NotImplementedError("Render method not implemented in inherited component.")

class TextContent(Content):

    def __init__(self, x: int, y: int, width: int):

        self.x = x
        self.y = y
        self.width = width

    def render(self, window: "Window", frame_count: int):

        