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

#
# Production configuration
#

env.key_filename = (expanduser(''),)
env.user = ''
env.known_hosts = ''
env.chef = '/usr/local/bin/chef-solo -c solo.rb -j node.json'
env.app_user = ''
env.project_dir = ''
env.activate = ''
env.branch = 'master'
env.AWS_SECRET_ACCESS_KEY = ''
env.AWS_ACCESS_KEY_ID = ''

def prod():
    """
    The production environment's configuration.
    """
    env.hosts = ("",)

#
# Production operations
#

def create_server(region='us-west-2',
    ami='ami-1cdd532c',
    key_name='ben-datadesk',
    instance_type='m1.medium',
    block_gb_size=12):
    """
    Spin up a new server on Amazon EC2.
    
    Returns the id and public address.
    
    By default, we use Ubuntu 12.04 LTS
    """
    print("Warming up...")
    conn = boto.ec2.connect_to_region(
        region,
        aws_access_key_id = env.AWS_ACCESS_KEY_ID,
        aws_secret_access_key = env.AWS_SECRET_ACCESS_KEY,
    )
    print("Reserving an instance...")
    bdt = boto.ec2.blockdevicemapping.BlockDeviceType(connection=conn)
    bdt.size = block_gb_size
    bdm = boto.ec2.blockdevicemapping.BlockDeviceMapping(connection=conn)
    bdm['/dev/sda1'] = bdt
    reservation = conn.run_instances(
        ami,
        key_name=key_name,
        instance_type=instance_type,
        block_device_map=bdm,
    )
    instance = reservation.instances[0]
    print('Waiting for instance to start...')
    # Check up on its status every so often
    status = instance.update()
    while status == 'pending':
        time.sleep(10)
        status = instance.update()
    if status == 'running':
        print('New instance "' + instance.id + '" accessible at ' + instance.public_dns_name)
    else:
        print('Instance status: ' + status)
    return (instance.id, instance.public_dns_name)


def install_chef():
    """
    Install all the dependencies to run a Chef cookbook
    """
    # Install dependencies
    sudo('apt-get update', pty=True)
    sudo('apt-get install -y git-core rubygems ruby ruby-dev', pty=True)
    # Screw ruby docs.
    sudo("echo 'gem: --no-ri --no-rdoc' > /root/.gemrc")
    sudo("echo 'gem: --no-ri --no-rdoc' > /home/ubuntu/.gemrc")
    # Install Chef
    sudo('gem install chef', pty=True)


def cook():
    """
    Update Chef cookbook and execute it.
    """
    sudo('mkdir -p /etc/chef')
    sudo('chown ubuntu -R /etc/chef')
    local('ssh -i %s -o "StrictHostKeyChecking no" -o "UserKnownHostsFile %s" %s@%s "touch /tmp"' % (
            env.key_filename[0],
            env.known_hosts,
            env.user,
            env.host_string
        )
    )
    local('rsync -e "ssh -i %s -o \'UserKnownHostsFile %s\'" -av ./chef/ %s@%s:/etc/chef' % (
            env.key_filename[0],
            env.known_hosts,
            env.user,
            env.host_string
        )
    )
    sudo('cd /etc/chef && %s' % env.chef, pty=True)


def restart_apache():
    """
    Restarts apache on both app servers.
    """
    sudo("/etc/init.d/apache2 reload", pty=True)


def restart_varnish():
    """
    Restarts apache on both app servers.
    """
    sudo("service varnish restart", pty=True)


def clean():
    """
    Erases pyc files from our app code directory.
    """
    env.shell = "/bin/bash -c"
    with cd(env.project_dir):
        sudo("find . -name '*.pyc' -print0|xargs -0 rm", pty=True)


def install_requirements():
    """
    Install the Python requirements.
    """
    _venv("pip install -r requirements.txt")


def pull():
    """
    Pulls the latest code from github.
    """
    _venv("git pull origin master;")


def syncdb():
    """
    Run python manage.py syncdb over on our prod machine
    """
    _venv("python manage.py syncdb")


def collectstatic():
    """
    Roll out the latest static files
    """
    _venv("rm -rf ./static")
    _venv("python manage.py collectstatic --noinput")


def manage(cmd):
    _venv("python manage.py %s" % cmd)


def _venv(cmd):
    """
    A wrapper for running commands in our prod virturalenv
    """
    with cd(env.project_dir):
        sudo(
            "%s && %s && %s" % (env.activate, env.activate, cmd),
            user=env.app_user
        )


def deploy():
    """
    Deploy the latest code and restart everything.
    """
    pull()
    with settings(warn_only=True):
        clean()
    install_requirements()
    restart_apache()

#
# Local operations
#


def update_templates(template_path='./templates'):
    """
    Download the latest template release and load it into your system.
    
    It will unzip to "./templates" where you run it.
    """
    with lcd(template_path):
        local("curl -O http://databank-cookbook.latimes.com/dist/templates/latest.zip")
        local("unzip -o latest.zip")
        local("rm latest.zip")


def generate_secret(length=50,
    allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'):
    """
    Generates secret key for use in Django settings.
    """
    key = ''.join(random.choice(allowed_chars) for i in range(length))
    print 'SECRET_KEY = "%s"' % key


def rmpyc():
    """
    Erases pyc files from current directory.

    Example usage:

        $ fab rmpyc

    """
    print("Removing .pyc files")
    with hide('everything'):
        local("find . -name '*.pyc' -print0|xargs -0 rm", capture=False)


def rs(port=8000):
    """
    Fire up the Django test server, after cleaning out any .pyc files.

    Example usage:
    
        $ fab rs
        $ fab rs:port=9000
    
    """
    with settings(warn_only=True):
        rmpyc()
    local("python manage.py runserver 0.0.0.0:%s" % port, capture=False)


def sh():
    """
    Fire up the Django shell, after cleaning out any .pyc files.

    Example usage:
    
        $ fab sh
    
    """
    rmpyc()
    local("python manage.py shell", capture=False)
