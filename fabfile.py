import os
import sys

from fabric.api import local
from fabric.contrib import django


project_name = '{{ project_name }}'
project_settings = project_name + '.settings'
django.settings_module(project_settings)
from django.conf import settings
from django.utils.termcolors import colorize

pwd = os.path.dirname(__file__)
gzip_path = '{0}/{1}/gzip/static/'.format(pwd, project_name)
static_path = '{0}/{1}/static/'.format(pwd, project_name)

media_s3_bucket = 'media-apps-cironline-org'
verbose_production_name = '' # what you want to call it when it goes live

# log statement to console with optional color (defaults to white)
log = lambda x, y="white": sys.stdout.write(colorize(x, fg=y))

"""
Set AWS_BUCKET_NAME, AWS_STAGING_BUCKET_NAME
in `settings/production.py`
"""
try:
    from {{ project_name }}.settings.production import (
        AWS_BUCKET_NAME,
        AWS_STAGING_BUCKET_NAME
    )
except ImportError:
    log("Please set AWS_BUCKET_NAME in production.py \
        before executing any deploy", "red")


"""
Development Tasks
============
"""

def bootstrap():
    """
    Run commands to setup a new project
    """

    try:
        local("pip install -r requirements/base.txt")
        local("pip install -r requirements/python2.txt")

        createdb() # create postgis database

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


def rs(port=8000):
    """
    Start development server and grunt tasks. Optionally, specify port
    """
    local("python manage.py rserver 0.0.0.0:%s" % port)


def grunt():
    """
    Run grunt tasks installed from Yeoman generator
    """
    local('cd {{ project_name }} && grunt')


def sh():
    """
    Run Django extensions shell
    """
    local('python manage.py shell_plus')


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

    log("\nHEADS UP! Make sure you add '{0}.apps.{1}' to \
        INSTALLED_APPS in settings/common.py\n".format(project_name, app_name))


def dumpdata(app_name=''):
    """
    Dump the data of an app in json format
    and store it in the fixtures directory
    """
    local("python manage.py dumpdata {0} > fixtures/{1}.json".format(
        app_name, app_name
    ))


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


def createdb():
    """
    Creates local database for project
    """
    local('createdb {0}'.format(project_name))

    if settings.USE_POSTGIS:
        local('echo "CREATE EXTENSION postgis;" | psql {0}'.format(
            project_name
        ))


def dropdb():
    """
    drops local database for project
    """
    local('echo "DROP DATABASE {0};" | psql postgres'.format(project_name))


def clear(app_name, model_name):
    """
    Remove a model from an application database
    """
    local("echo 'DROP TABLE {0}_{1};' | psql {{project_name}}".format(
        app_name, model_name
    ))


def destroy():
    """
    destoys the database and django project. Be careful!
    """
    log("You are about to mothball this entire project. \
        Sure you want to do that? <enter 'Y' or 'N'>", "red")
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
"""
Deployment Tasks
================
"""

def gzip_assets():
    """
    GZips every file in the assets directory and places the new file
    in the gzip directory with the same filename.
    """
    local("cd {0}; python ./lib/gzip_assets.py".format(pwd))

def grunt_build():
    """
    Execute grunt build for any cleanup that
    needs to happen before deploying to s3
    """
    local('cd {{ project_name }} && grunt build')


def deploy_to_s3():
    """
    Deploy the latest project site media to S3.
    Path options:
    use `gzip_path` if gziping assets (default)
    use `static_path` if not e.g.

    local('s3cmd -P --guess-mime-type sync {1} \
        s3://{2}/{3}/'.format(pwd, static_path, media_s3_bucket, project_name))

    """
    local('s3cmd -P --add-header=Content-encoding:gzip \
        --guess-mime-type --rexclude-from={0}/s3exclude sync {1} \
        s3://{2}/{3}/'.format(pwd, gzip_path, media_s3_bucket, project_name))

def publish():
    """publish build from django bakery to s3"""
    # add --cf-invalidate if pushing to bucket with Cloudfront caching
    local('s3cmd -P \
        sync {0}/{1}/build/ s3://{2}/{3}/'.format(
            pwd,
            project_name,
            AWS_STAGING_BUCKET_NAME,
            verbose_production_name
        )
    )

def build():
    """shortcut for django bakery build command"""
    local('python manage.py build \
        --skip-static --settings={{ project_name }}.settings.production')

def unbuild():
    """shortcut for django bakery unbuild command"""
    local('python manage.py unbuild \
        --settings={{ project_name }}.settings.production')

def compress():
    """shortcut for django compressor offline compression command"""
    local('python manage.py compress \
        --settings={{ project_name }}.settings.production')

def reset():
    """delete all the deploy code"""
    local('cd {{ project_name }} && \
        rm -rf static && rm -rf gzip && rm -rf build')

def deploy():
    reset()
    compress()
    build()

    if settings.USE_GRUNT:
        grunt_build()
        
    gzip_assets()
    deploy_to_s3()
    publish()
