import subprocess

from django.core.management.base import BaseCommand
from django.core import management
from django.conf import settings


class Command(BaseCommand):
    help = "Runs `compass --watch` and `collectstatic` before launching Django's own runserver"

    def handle(self, *args, **options):
        self.start_compass_watch()

        # `interactive = False` is the undocumented equivalent of the '--no-input' flag,
        # which we can't use in a management command. See http://stackoverflow.com/a/9999429/8438
        management.call_command('collectstatic', interactive = False)

        # Allow specifying an IP:port string, if provided
        if args:
            management.call_command('runserver', args[0])
        else:
            management.call_command('runserver')

    def start_compass_watch(self):
        self.stdout.write(self.style.NOTICE(">>> Compass is watching %r") % settings.COMPASS_INPUT_PATH + "\n" )
        self.stdout.write(self.style.NOTICE(">>> Generated CSS is at %r") % settings.COMPASS_OUTPUT_PATH + "\n" )
        self.compass_process = subprocess.Popen(
            ['compass watch --sass-dir %s --css-dir %s' % (settings.COMPASS_INPUT_PATH, settings.COMPASS_OUTPUT_PATH)],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=self.stdout,
            stderr=self.stderr,
        )
        self.stdout.write(self.style.NOTICE(">>> Compass watch process on pid %r" % self.compass_process.pid) + "\n")
