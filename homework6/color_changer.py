from colorama import Fore


class Color_Changer:
    my_colors = {
        'red': Fore.RED,
        'yellow': Fore.YELLOW,
        'green': Fore.GREEN,
        'blue': Fore.BLUE,
        'white': Fore.LIGHTWHITE_EX,
        'gray': Fore.LIGHTBLACK_EX,
        'black': Fore.BLACK,
        'purple': Fore.MAGENTA,
    }

    def __init__(self, foreground_color):
        self.foreground_color = foreground_color

    @classmethod
    def print_colors(cls, color):
        return color in cls.my_colors.keys()

    def __enter__(self):
        if self.print_colors(self.foreground_color.lower()):
            print(self.my_colors[self.foreground_color.lower()], end='')
            return None
        else:
            print('Can`t colorize your message. There is no such color available!')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(Fore.RESET, end='')


if __name__ == '__main__':
    with Color_Changer('GrEeN'):
        print('Some colorized text')
    print('Default color text')
