from setuptools import setup
from distutils.core import Command

import django
from django.conf import settings
from django.core.management import call_command


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        settings.configure(
            DATABASES={
                'default': {
                    'NAME': ':memory:',
                    'ENGINE': 'django.db.backends.sqlite3'
                }
            },
            INSTALLED_APPS=(
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.admin',
                'lib',
            ),
            MIDDLEWARE_CLASSES = (
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
            )
        )

        django.setup()
        call_command('test', 'lib')


setup(
    name='django-project-template',
    cmdclass={'test': TestCommand}
)
