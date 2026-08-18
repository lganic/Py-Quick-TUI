def overflow_text_animation(text: str, frame_count: int, available_size: int, frozen_frames: int = 10, speed = .1):

    # Runs the sliding text animation.

    if len(text) <= available_size:
        return text # We've got enough space. Return the string as is.

    available_size -= 1 # For ellipsis

    frame_count = round(frame_count * speed)

    # Okay, we need to do the animation.
    # This is just based on the function x - k * floor(x / k) but with frozen sections at the beginning and end.

    needed_frames = len(text) - available_size

    animation_length = needed_frames + 2 * frozen_frames

    animation_point = frame_count - animation_length * (frame_count // animation_length) - frozen_frames

    animation_point = min(needed_frames, max(0, animation_point))

    if animation_point != len(text) - available_size:

        return text[animation_point: animation_point + available_size] + "…"

    return text[animation_point: animation_point + available_size] + " "