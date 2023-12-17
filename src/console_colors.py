from __future__ import annotations

from colorama import Back
from colorama import Fore
from colorama import init
from colorama import Style

init()


def blue_var(var: str) -> str:
    return f'{Fore.BLUE}{Style.BRIGHT}{var}{Style.RESET_ALL}'


def cyan_input():
    print(Fore.CYAN + Style.BRIGHT + '', end='')
    input_colored = input()
    print(Style.RESET_ALL, end='')
    return input_colored


def yellow_warning() -> str:
    return f'{Back.YELLOW}{Style.BRIGHT}[WARNING]{Style.RESET_ALL}'


def green_done() -> str:
    return f'{Back.GREEN}{Style.BRIGHT}[DONE]{Style.RESET_ALL}'


def red_error() -> str:
    return f'{Back.RED}[ERROR]{Style.RESET_ALL}'
