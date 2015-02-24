from fabric.api import local, task

@task
def bower(command, args, option):
    """
    usage: fab bower:<command>, <args>, <option>

    Execute bower commands.

    See 'fab bower:help' for more information
    """
    local('cd {{ project_name }} && bower {0} {1} {2}'.format(
        command,
        args,
        option
    ))


@task
def npm(command, args, option):
    """
    usage: fab npm:<command>, <option>, <args>

    Execute npm commands

    See 'fab npm:help' for more information
    """
    local('cd {{ project_name }} && npm {0} {1} {2}'.format(
        command,
        option,
        args,
    ))


@task
def scaffold():
    """
    Setup frontend management for Django project with yo, grunt and bower.
    See 'https://github.com/cirlabs/generator-newsapp' for more information.
    """
    npm('install', 'yo', '-g')
    npm('install', 'generator-newsapp', '-g')
    local('cd {{ project_name }} && yo newsapp')
