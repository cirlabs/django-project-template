from __future__ import with_statement

import os
import sys
import boto
import random
from fabric.api import *
from os.path import expanduser
from boto.ec2.connection import EC2Connection

# vars
pwd = os.path.dirname(__file__)
project_name = "{{ project_name }}"
gzip_path = '{0}/{1}/gzip/static/'.format(pwd, project_name)
site_media_prefix = "site_media"
production_domain = 'apps.cironline.org' # prompt to define this
s3_bucket = 'media.{0}'.format(production_domain)


sys.path.append(pwd)

# Environment

def production():
  """
  Work on production environment
  """
  env.settings = 'production'

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

def get_node_libs():
  """
  Install Node.js for Mac OS X or Ubuntu Linux
  """
  print ("Are you running this on Mac OS X or Ubuntu Linux? <Answer 'Mac' or 'Linux'>")
  platform = raw_input("> ")
  if (platform.upper() == 'MAC'):
    local('npm install -g yo grunt-cli bower generator-newsapp')
  elif (platform.upper() == 'LINUX'):
    local('sudo npm install -g yo grunt-cli bower generator-newsapp')
  else:
    print ("Error: you did not answer 'Mac' or 'Linux'")
    get_node_libs()

def yo():
  """
  Run yeoman generator to scaffold front-end dependencies
  """
  local('cd {0} && yo newsapp'.format(project_name))

def install_node():
  """
  Install node.js for Mac OS X or Ubuntu Linux
  """
  print ("Installing Node, eh? Mac or Linux? <answer 'Mac' or 'Linux'>")

  answer = raw_input("> ")
  if (answer.upper() == 'MAC'):
    print ("Installing Node with Homebrew. Is Homebrew installed?")
    while True:
      answer = raw_input("> ")
      if (answer.upper() == 'Y'):

        local("brew install node")
        break

      elif (answer.upper() == 'N'):
        local('ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go/install)"')
        local("brew install node")
        break

      else:
        print ("You did not answer 'Y' or 'N'.")

  elif (answer.upper() == 'LINUX'):
    local("sudo apt-get update")
    local("sudo apt-get install -y python-software-properties python g++ make")
    local("sudo add-apt-repository -y ppa:chris-lea/node.js")
    local("sudo apt-get update")
    local("sudo apt-get install nodejs")

  else:
    print("You didn't answer Mac or Linux")
    install_node()

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

def startapp(app_name=''):
  """
  Create django app
  """
  local("python manage.py startapp {0}".format(app_name))
  local("mv {0} {1}/apps/".format(app_name, project_name))
  print("\nHEADS UP! Make sure you add '{0}.apps.{1}' to INSTALLED_APPS in settings/common.py\n".format(project_name, app_name))

def createdb():
  """
  Creates local database for project
  """
  local('createdb {0}'.format(project_name))
  local('echo "CREATE EXTENSION postgis;" | psql {0}'.format(project_name))

def dropdb():
  """
  drops local database for project
  """
  local('echo "DROP DATABASE {0};" | psql postgres'.format(project_name))

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

def deploy_to_s3():
    """
    Deploy the latest project site media to S3.
    """
    local('s3cmd -P --add-header=Content-encoding:gzip --guess-mime-type --rexclude-from={0}/s3exclude sync {1} s3://{2}/{3}/{4}/'.format(localpath, gzip_path, s3_bucket, project_name, site_media_prefix))

def deploy_static():
    local("python ./{0}/manage.py collectstatic".format(project_name))
    gzip_assets()
    deploy_to_s3()