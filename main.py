import sys

from enum import Enum


from discord_reader import run as discord_run
from console_reader import run as console_run


class Module(Enum):
    DISCORD = "discord"
    CONSOLE = "console"


def main(module: Module):
    if module == Module.DISCORD:
        discord_run()
    elif module == Module.CONSOLE:
        console_run()


if __name__ == '__main__':
    module_name = sys.argv[-1]
    main(Module(module_name))
