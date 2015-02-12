import sys
from django.utils.termcolors import colorize


def log(string, color="white"):
    """
    write string to stdout with color. Default color is white.
    """
    sys.stdout.write(
        colorize(string, fg=color)
    )
