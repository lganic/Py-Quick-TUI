from enum import Enum

class DetailMode(Enum):

    BASIC = 1
    DOUBLE = 2
    BOLDED = 3
    CURVED = 4

# Indexing in binary. 1 = top 2 = right 4 = bottom 8 = left
_CORNER_TABLE = {
    DetailMode.BASIC: (
        '╳', # This shouldn't be used. It would be the case that happens if nothing is connected to a corner. Maybe do a space here instead? Idk. This should be a weird enough char to show that something has gone wrong.
        '│', # Not perfect. Should be half size, but that char doesn't exist afaik
        '─', # Not perfect. Should be half size, but that char doesn't exist afaik
        '└',
        '│', # Not perfect. Should be half size, but that char doesn't exist afaik
        '│',
        '┌',
        '├',
        '─', # Not perfect. Should be half size, but that char doesn't exist afaik
        '┘',
        '─',
        '┴',
        '┐',
        '┤',
        '┬',
        '┼'
    ),
    DetailMode.DOUBLE: (
        '╳', # This shouldn't be used. It would be the case that happens if nothing is connected to a corner. Maybe do a space here instead? Idk. This should be a weird enough char to show that something has gone wrong.
        '║', # Not perfect. Should be half size, but that char doesn't exist afaik
        '═', # Not perfect. Should be half size, but that char doesn't exist afaik
        '╚',
        '║', # Not perfect. Should be half size, but that char doesn't exist afaik
        '║',
        '╔',
        '╠',
        '═', # Not perfect. Should be half size, but that char doesn't exist afaik
        '╝',
        '═',
        '╩',
        '╗',
        '╣',
        '╦',
        '╬'
    ),
    DetailMode.BOLDED: (
        '╳', # This shouldn't be used. It would be the case that happens if nothing is connected to a corner. Maybe do a space here instead? Idk. This should be a weird enough char to show that something has gone wrong.
        '┃', # Not perfect. Should be half size, but that char doesn't exist afaik
        '━', # Not perfect. Should be half size, but that char doesn't exist afaik
        '┗',
        '┃', # Not perfect. Should be half size, but that char doesn't exist afaik
        '┃',
        '┏',
        '┣',
        '━', # Not perfect. Should be half size, but that char doesn't exist afaik
        '┛',
        '━',
        '┻',
        '┓',
        '┫',
        '┳',
        '╋'
    ),
    DetailMode.CURVED: (
        '╳', # This shouldn't be used. It would be the case that happens if nothing is connected to a corner. Maybe do a space here instead? Idk. This should be a weird enough char to show that something has gone wrong.
        '│', # Not perfect. Should be half size, but that char doesn't exist afaik
        '─', # Not perfect. Should be half size, but that char doesn't exist afaik
        '╰',
        '│', # Not perfect. Should be half size, but that char doesn't exist afaik
        '│',
        '╭',
        '├', # This curved char does not exist afaik. Using basic.
        '─', # Not perfect. Should be half size, but that char doesn't exist afaik
        '╯',
        '─',
        '┴', # This curved char does not exist afaik. Using basic.
        '╮',
        '┤', # This curved char does not exist afaik. Using basic.
        '┬', # This curved char does not exist afaik. Using basic.
        '┼' # This curved char does not exist afaik. Using basic.
    ),
}

def get_connected_char(top_connected: bool, bottom_connected: bool, left_connected: bool, right_connected: bool, detail: DetailMode = DetailMode.BASIC):

    index = \
        1 if top_connected    else 0 + \
        2 if right_connected  else 0 + \
        4 if bottom_connected else 0 + \
        8 if left_connected   else 0
    
    return _CORNER_TABLE[detail][index]

def get_wall_char(vertical: bool, detail: DetailMode = DetailMode.BASIC):

    return get_connected_char(
        top_connected = vertical,
        bottom_connected = vertical,
        left_connected = not vertical, 
        right_connected = not vertical,
        detail = detail
    )