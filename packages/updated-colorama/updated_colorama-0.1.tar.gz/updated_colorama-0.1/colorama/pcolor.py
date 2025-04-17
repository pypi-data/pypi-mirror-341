import os
import time
from colorama import Fore, Style, init

init()

def color_generator():
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.MAGENTA]
    while True:
        yield from colors

def pcolor(text):
    color_gen = color_generator()
    try:
        while True:
            color = next(color_gen)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Style.RESET_ALL + color + text)
            time.sleep(1)
    except KeyboardInterrupt:
        print(Style.RESET_ALL)
        return
