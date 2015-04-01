import sys
import os
import fnmatch

from django.utils.termcolors import colorize


def log(string, color="white"):
    """
    write string to stdout with color. Default color is white.
    """
    sys.stdout.write(
        colorize(string, fg=color)
    )


def all_files(root, patterns='*', single_level=False, yield_folders=False):
    """
    Expand patterns form semicolon-separated string to list
    example usage: thefiles = list(all_files('/tmp', '*.py;*.htm;*.html'))
    """
    patterns = patterns.split(';')

    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)

        files.sort()

        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    yield os.path.join(path, name)
                    break

        if single_level:
            break
