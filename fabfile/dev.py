import os

from lib.utils import log

from fabric.api import local, task
from fabric.contrib import django

django.settings_module("{{ project_name }}.settings")
from django.conf import settings

"""
Development Tasks
============
"""

project_name = "{{ project_name }}"


@task
def rs(port=8000):
    """
    Start development server and grunt tasks. Optionally, specify port
    """
    local("python manage.py rserver 0.0.0.0:%s" % port)


@task
def sh():
    """
    Run Django extensions shell
    """
    local('python manage.py shell_plus')


@task
def startapp(app_name=''):
    """
    Create django app
    """
    # create django app and move to apps
    local("python manage.py startapp {0}".format(app_name))
    local("mv {0} {1}/apps/".format(app_name, project_name))

    # make managment command directory
    local("mkdir {0}/apps/{1}/management".format(project_name, app_name))
    local("mkdir {0}/apps/{1}/management/commands".format(
        project_name, app_name
        )
    )
    local("touch {0}/apps/{1}/management/__init__.py".format(
        project_name, app_name
        )
    )
    local("touch {0}/apps/{1}/management/commands/__init__.py".format(
        project_name, app_name
        )
    )

    log("\nHEADS UP! Make sure you add '{0}.apps.{1}' ".format(
        project_name, app_name))
    log("to INSTALLED_APPS in settings/common.py")


@task
def dumpdata(app_name=''):
    """
    Dump data of an app in JSON format and store in the fixtures directory
    """
    if app_name is not '':
        fixtures_dir = os.path.join(settings.ROOT_DIR, app_name, 'fixtures')

        if not os.path.exists(fixtures_dir):
            os.makedirs(fixtures_dir)

        local("python manage.py dumpdata {0} > {1}/{2}.json".format(
            app_name, fixtures_dir, app_name
            )
        )
    else:
        log("please specify an app name", "red")


@task
def loaddata(app_name=''):
    """
    load the data of an app in json format
    and store it in the fixtures directory
    """
    if app_name is not '':
        fixtures_dir = os.path.join(
            settings.ROOT_DIR,
            app_name,
            'fixtures',
            "{0}.json".format(app_name)
        )

        local("python manage.py loaddata {0}".format(fixtures_dir))

    else:
        log("please specify an app name", "red")


@task
def createdb():
    """
    Creates local database for project
    """
    log("creating database")
    local('createdb {0}'.format(project_name))

    if settings.USE_POSTGIS:
        local('echo "CREATE EXTENSION postgis;" | psql {0}'.format(
            project_name
            )
        )


@task
def dropdb():
    """
    drops local database for project
    """
    local('echo "DROP DATABASE {0};" | psql postgres'.format(project_name))


@task
def clear(app_name, model_name):
    """
    Remove a model from an application database
    """
    local("echo 'DROP TABLE {0}_{1};' | psql {{project_name}}".format(
        app_name, model_name
        )
    )


@task
def destroy():
    """
    destoys the database and django project. Be careful!
    """
    log("You are about to mothball this entire project.\n", "red")
    log("Sure you want to do that? <enter 'Y' or 'N'>", "red")
    while True:
        answer = raw_input("> ")
        if (answer.upper() == 'Y'):
            dropdb()
            local('cd .. && rm -rf {0}'.format(project_name))
            break

        elif (answer.upper() == 'N'):
            log("cancelling destory")
            break

        else:
            log("You didn't answer 'Y' or 'N'")


@task()
def bootstrap():
    """
    DEFAULT: Run commands to setup a new project
    """

    try:
        local("pip install -r requirements/base.txt")
        local("pip install -r requirements/python2.txt")

        createdb()  # create postgis database

        local("python manage.py migrate")

        log(
            "Success! Now run `fab rs` to start the development server",
            "green"
        )
    except Exception, e:
        log(
            "Uh oh! Something went wrong. Double check your settings. Error:",
            "red"
        )

        raise e
