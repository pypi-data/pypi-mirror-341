from colorama import DarkFore, Style, init
init()

def print_dark_colors():
    print(DarkFore.DARK_RED + "Dark Red" + Style.RESET_ALL)
    print(DarkFore.DARK_GREEN + "Dark Green" + Style.RESET_ALL)
    print(DarkFore.DARK_YELLOW + "Dark Yellow" + Style.RESET_ALL)
    print(DarkFore.DARK_BLUE+ "Dark Blue" + Style.RESET_ALL)
    print(DarkFore.DARK_MAGENTA + "Dark Magenta" + Style.RESET_ALL)
    print(DarkFore.DARK_CYAN + "Dark Cyan" + Style.RESET_ALL)
    print(DarkFore.DARK_WHITE + "Dark White" + Style.RESET_ALL)

print_dark_colors()
