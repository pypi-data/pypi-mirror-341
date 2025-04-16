red = "\033[91m"
reset = "\033[0m"
black   = "\033[30m"
red     = "\033[31m"
green   = "\033[32m"
yellow  = "\033[33m"
blue    = "\033[34m"
magenta = "\033[35m"
cyan    = "\033[36m"
white   = "\033[37m"

def set_red(text):
    red_text = red + text + reset
    return red_text

def set_blue(text):
    blue_text = blue + text + reset
    return blue_text

def set_green(text):
    green_text = green + text + reset
    return green_text

def set_red(text):
    red_text = red + text + reset
    return red_text

def set_cyan(text):
    cyan_text = cyan + text + reset
    return

def set_magenta(text):
    magenta_text = magenta + text + reset
    return magenta_text

def set_white(text):
    white_text = white + text + reset
    return white_text

def set_yellow(text):
    yellow_text = yellow + text + reset
    return yellow_text

def default_color(text):
    default_text = reset + text + reset
    return default_text
    