from __future__ import with_statement

import os
import sys
import boto
import random
from fabric.api import *
from os.path import expanduser
from boto.ec2.connection import EC2Connection

pwd = os.path.dirname(__file__)
sys.path.append(pwd)

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

def get_node_libs():
  """
  Install Node.js for Mac OS X or Ubuntu Linux
  """
  print ("Are you running this on Mac OS X or Ubuntu Linux? <Answer 'Mac' or 'Linux'>")
  platform = raw_input("> ")
  if (platform.upper() == 'MAC'):
    local('npm install -g yo grunt-cli bower')
    #local('npm install -g git@github.com:cirlabs/generator-newsapp.git')
  elif (platform.upper() == 'LINUX'):
    sudo('npm install -g yo grunt-cli bower')
    #sudo('npm install -g git@github.com:cirlabs/generator-newsapp.git')
  else:
    print ("Error: you did not answer 'Mac' or 'Linux'")
    get_node_libs()

def yo():
  """
  Run yeoman generator to scaffold front-end dependencies
  """
  local('cd {{ project_name }} && yo newsapp')

def install_node():
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
    sudo("apt-get update")
    sudo("apt-get install -y python-software-properties python g++ make")
    sudo("add-apt-repository -y ppa:chris-lea/node.js")
    sudo("apt-get update")
    sudo("apt-get install nodejs")

  else:
    print("You didn't answer Mac or Linux")
    install_node()

def rs():
  """
  Start development server
  """
  local("python manage.py runserver")

def startapp(appname=''):
  """
  Create django app
  """
  local("python manage.py startapp %s" % appname)

def createdb():
  """
  Creates local database for project
  """
  local('createdb {{ project_name }}')
  local('echo "CREATE EXTENSION postgis;" | psql {{ project_name }}')

def dropdb():
  """
  drops local database for project
  """
  local('echo "DROP DATABASE {{ project_name }};" | psql postgres')