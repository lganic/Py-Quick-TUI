from dataclasses import dataclass
from typing import TYPE_CHECKING
from .animations import overflow_text_animation

if TYPE_CHECKING:
    from .window import Window

@dataclass
class RenderSpace:
    x: int
    y: int
    width: int
    height: int

    def valid(self):
        return self.width > 0 and self.height > 0

class Content:

    def render(self, target_window: "Window", frame_count: int, space: RenderSpace) -> RenderSpace:

        raise NotImplementedError("Render method not implemented in inherited component.")

class TextContent(Content):

    def __init__(self, text: str):

        self.text = text

    def render(self, target_window: "Window", frame_count: int, space: RenderSpace) -> RenderSpace:

        animated_text = overflow_text_animation(self.text, frame_count, space.width)

        target_window.put_text(space.x, space.y, animated_text)

        return RenderSpace(
            space.x,
            space.y,
            len(animated_text),
            1
        )