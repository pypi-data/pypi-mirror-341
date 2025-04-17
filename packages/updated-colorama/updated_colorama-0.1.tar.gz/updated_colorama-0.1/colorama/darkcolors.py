from colorama import Style, Fore, Back, init
init()
# Dark red 163, 51, 51
# Dark green 66, 163, 51
# Dark yellow 172, 181, 38
# Dark blue 58, 49, 140
# Dark magenta 125, 42, 113
# Dark white 133, 127, 131
# Dark cyan 42, 113, 125

class DarkFore:
    DARK_RED = '\033[38;2;163;51;51m'
    DARK_GREEN = '\033[38;2;66;163;51m'
    DARK_YELLOW = '\033[38;2;172;181;38m'
    DARK_BLUE = '\033[38;2;58;49;140m'
    DARK_MAGENTA = '\033[38;2;125;42;113m'
    DARK_CYAN = '\033[38;2;133;127;131m'
    DARK_WHITE = '\033[38;2;42;113;125m'
