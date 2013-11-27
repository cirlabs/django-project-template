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
  print ("Need to install the node dependencies? <'y' or 'n'>")
  while True:
    answer = raw_input("> ")

    if (answer.upper() == 'Y'):
      install_node_dependencies()
      break

    elif (answer.upper() == 'N'):
      print ("Skipping dependency install")
      break

    else:
      print ("Error: you did not answer 'y' or 'n'")

  run_yeoman_scaffold()

def install_node_dependencies():
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
    install_node_dependencies()

def run_yeoman_scaffold():
  local('cd {{ project_name }} && yo newsapp')

def rs():
  local('python manage.py runserver')