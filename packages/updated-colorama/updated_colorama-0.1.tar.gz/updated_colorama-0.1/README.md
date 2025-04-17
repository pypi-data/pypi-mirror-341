# Перед прочтением
Некоторые функции библиотеки могут не работать на Python 2

# updated-colorama
colorama - отличная библиотека для написания цветных текстов. Так почему бы не улучшить ее?

Библиотека представляет расширенные возможности для написания цветных текстов.

# Установка
Установить библиотеку можно по команде:
pip install updated_colorama

# Функции
Ниже будут прописаны все функции которые предоставляет библиотека

# Оранжевый текст
В оригинальной colorama нету встроенной поддержки оранжевого текста. Но тут она есть!

Пример использования:

from colorama import OrangeText, Style, init

init()

print(OrangeText.ORANGE + "Оранжевый текст" + Style.RESET_ALL)
# Почему надо указывать colorama, а не updated_colorama?
Я по другому не смог сделать

# Темные цвета
В colorama нету встроенной поддержки темных цветов. Но тут она есть!

Пример использования:

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

Здесь показываются все темные цвета которые есть в библиотеке

# Переливание цветов
Теперь вы можете сделать переливающийся текст!

Пример использования:

from colorama import pcolor
pcolor("Test")
# Авторские права
Авторские права принадлежат Jonathan Hartley

Загляните в Корневая папка библиотеки/colorama/copyright.py