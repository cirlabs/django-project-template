from __future__ import with_statement

import os
import sys
import boto
import random
from os.path import expanduser
from boto.ec2.connection import EC2Connection

from fabric.api import *
from fabric.contrib import django

django.project('{{project_name}}')
from {{project_name}}.settings import common as settings
from {{project_name}}.settings.production import AWS_BUCKET_NAME

# vars
pwd = os.path.dirname(__file__)
project_name = "{{ project_name }}"
gzip_path = '{0}/{1}/gzip/static/'.format(pwd, project_name)
site_media_prefix = "site_media"
production_domain = 'apps.cironline.org' # prompt to define this
s3_bucket = AWS_BUCKET_NAME
media_s3_bucket = 'media-apps-cironline-org'
s3_directory = project_name

verbose_production_name = 'hired-guns' # what you want to call it when it goes live


sys.path.append(pwd)


# Setup and install

def setup():
    """
    Fetch required dependencies and setup the front-end
    """
    print ("Do you need to install the project's node.js dependencies (Yo, Bower, Grunt)? <'y' or 'n'>")
    while True:
        answer = raw_input("> ")

        if (answer.upper() == 'Y'):
          get_node_libs()
          break

        elif (answer.upper() == 'N'):
          print ("Skipping dependency install")
          break

        else:
          print ("Error: you did not answer 'y' or 'n'")

    yo()
    createdb()

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
    local("python manage.py startapp {0}".format(app_name))
    local("mv {0} {1}/apps/".format(app_name, project_name))
    print("\nHEADS UP! Make sure you add '{0}.apps.{1}' to INSTALLED_APPS in settings/common.py\n".format(project_name, app_name))

def dumpdata(app_name=''):
    """
    Dump the data of an app in json format and store it in the fixtures directory
    """
    local("python manage.py dumpdata {0} > fixtures/{1}.json".format(app_name, app_name))

def loaddata(app_name=''):
    """
    Dump the data of an app in json format and store it in the fixtures directory
    """
    if app_name is not '':
        fixtures_dir = os.path.join(settings.ROOT_DIR, app_name, 'fixtures', "{0}.json".format(app_name))
        local("python manage.py loaddata {0}".format(fixtures_dir))

    else:
        print "please specify an app name"

def createdb():
    """
    Creates local database for project
    """
    local('createdb {0}'.format(project_name))

    if settings.USE_POSTGIS:
        local('echo "CREATE EXTENSION postgis;" | psql {0}'.format(project_name))

def dropdb():
    """
    drops local database for project
    """
    local('echo "DROP DATABASE {0};" | psql postgres'.format(project_name))

def clear(app_name, model_name):
    """
    Remove a model from an application database
    """
    local("echo 'DROP TABLE %s_%s;' | psql {{project_name}}" % (app_name, model_name))

def destroy():
    """
    destoys the database and django project. Be careful!
    """
    print("You are about to mothball this entire project. Sure you want to do that? <enter 'Y' or 'N'>")
    while True:
        answer = raw_input("> ")
        if (answer.upper() == 'Y'):
            dropdb()
            local('cd .. && rm -rf {0}'.format(project_name))
            break

        elif (answer.upper() == 'N'):
            print("cancelling destory")
            break

        else:
            print("You didn't answer 'Y' or 'N'")

# Static media
# This should all run after a grunt task runs to collect the deps used
def gzip_assets():
    """
    GZips every file in the assets directory and places the new file
    in the gzip directory with the same filename.
    """
    local("cd {0}; python ./gzip_assets.py".format(pwd))

def grunt_build():
    """Execute grunt build for any cleanup that needs to happen before deploying to s3"""
    local('cd {{ project_name }} && grunt build')

def deploy_to_s3():
    """
    Deploy the latest project site media to S3.
    """
    local('s3cmd -P --add-header=Content-encoding:gzip --guess-mime-type --rexclude-from={0}/s3exclude sync {1} s3://{2}/{3}/'.format(localpath, gzip_path, s3_bucket, project_name))

def publish():
    """publish build from django bakery to s3"""
    local('s3cmd -P sync /home/aaron/Code/{{ project_name }}/{{ project_name }}/build/ s3://apps.cironline.org/hacienda/')

def build():
    """shortcut for django bakery build command"""
    local('python manage.py build --skip-static --settings={{ project_name }}.settings.production')

def unbuild():
    """shortcut for django bakery unbuild command"""
    local('python manage.py unbuild --settings={{ project_name }}.settings.production')

def compress():
    """shortcut for django compressor offline compression command"""
    local('python manage.py compress --settings={{ project_name }}.settings.production')

def reset():
    """delete all the deploy code"""
    local('cd {{ project_name }} && rm -rf static && rm -rf gzip && rm -rf build')

def deploy():
    reset()
    compress()
    build()
    gzip_assets()
    grunt_build()
    deploy_to_s3()
    publish()
