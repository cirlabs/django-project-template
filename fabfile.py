import os
import sys

import boto
from boto.s3.key import Key
from fabric.api import local
from fabric.contrib import django

django.settings_module("{{ project_name }}.settings")
from django.utils.termcolors import colorize
from django.conf import settings

from {{ project_name }}.settings.production import (
    AWS_BUCKET_NAME, AWS_MEDIA_BUCKET_NAME,AWS_STAGING_BUCKET_NAME, BUILD_DIR)

project_name = "{{ project_name }}"
pwd = os.path.dirname(__file__)
gzip_path = '{0}/{1}/gzip/static/'.format(pwd, project_name)
static_path = '{0}/{1}/static/'.format(pwd, project_name)
verbose_app_name = None # what you want to call it when it goes live

s3 = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
s3_bucket = s3.get_bucket(AWS_BUCKET_NAME)
s3_media_bucket = s3.get_bucket(AWS_MEDIA_BUCKET_NAME)
s3_staging_bucket = s3.get_bucket(AWS_STAGING_BUCKET_NAME)

# log statement to console with optional color (defaults to white)
log = lambda x, y="white": sys.stdout.write(colorize(x, fg=y))

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
    Deploy project to S3.

    Path options:
    use `gzip_path` if gziping assets (default)
    use `static_path` if not e.g.
    """
    # See: https://gist.github.com/SavvyGuard/6115006

    def percent_cb(complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()


    # max size in bytes for uploading in parts. between 1 and 5 GB recommended
    MAX_SIZE = 20 * 1000 * 1000

    # size of parts when uploading in parts
    PART_SIZE = 6 * 1000 * 1000

    # paths
    dest_dir = verbose_app_name if verbose_app_name else project_name

    app_directory = BUILD_DIR

    source_dir = settings.STATIC_ROOT

    upload_file_names = []
    app_directory_file_names = []

    # Grab files
    for dir_, _, files in os.walk(source_dir):
        for filename in files:
            relative_directory = os.path.relpath(dir_, source_dir)
            relative_file = os.path.join(relative_directory, filename)

            upload_file_names.append(relative_file)

    for (app_directory, dirname, filename) in os.walk(app_directory):
        app_directory_file_names.extend(filename)

    # Upload static media
    for filename in upload_file_names:
        source_path = os.path.join( settings.STATIC_ROOT, filename )
        dest_path = os.path.join(dest_dir, filename)

        log("  Uploading {0} to bucket {1}".format(
            source_path,
            AWS_MEDIA_BUCKET_NAME
            )
        )

        filesize = os.path.getsize(source_path)

        if filesize > MAX_SIZE:
            log("    Large file. Running multipart upload")
            mp = s3_media_bucket
            fp = open(source_path, 'rb')
            fp_num = 0
            while (fp.tell() < filesize):
                fp_num += 1
                log("      uploading part %i" % fp_num)
                mp.upload_part_from_file(
                    fp, fp_num, cb=percent_cb, num_cb=10, size=PART_SIZE)

                mp.complete_upload()

        else:
            log("    Running upload")
            k = Key(s3_media_bucket)
            k.key = dest_path
            k.set_contents_from_filename(source_path, cb=percent_cb, num_cb=10)
            k.make_public()

    # Upload build files
    for filename in app_directory_file_names:
        source_path = os.path.join( BUILD_DIR, filename )
        dest_path = os.path.join(dest_dir, filename)

        k = Key(s3_staging_bucket)
        k.key = dest_path
        k.set_contents_from_filename(source_path, cb=percent_cb, num_cb=10)
        k.make_public()

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
    settings.USE_GRUNT and grunt_build()
    deploy_to_s3()
