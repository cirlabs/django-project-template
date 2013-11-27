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

def hello():
  print ("Helloooooooooooooooo, Wooooooooooooooooorld")