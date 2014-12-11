# Django Project Template [![Build Status](https://secure.travis-ci.org/cirlabs/django-project-template.png?branch=master)](http://travis-ci.org/cirlabs/django-project-template)

No longer a fork, but a state of mind :thumbsup:

Part of CIRs three-part deploy:

![Three Amigos](http://collider.com/wp-content/uploads/three-amigos-blu-ray-slice.jpg)

[ops](https://github.com/BayCitizen/ops) | [**django-project-template**](https://github.com/cirlabs/django-project-template) | [generator-newsapp](https://github.com/cirlabs/generator-newsapp/)


## Requirements
- [Django 1.6](https://www.djangoproject.com/)
- [Postgres 9.x](http://www.postgresql.org/)
- [PostGIS 2.0](http://postgis.net/)
- [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/)

If you want to scaffold the front-end, you'll also need:

- [Node.js 0.8.x](http://nodejs.org/)
- [npm](http://npmjs.org/) (usually installed with Node)
- [Grunt.js](http://gruntjs.com)
- [Bower](http://bower.io/)
- [Yeoman](http://yeoman.io/index.html)

## Kick off

Create virtualenv

```bash
$ mkvirtualenv project_name --no-site-packages
```

Install Django

```bash
$ pip install django==1.6
```

Create django project with this template
```bash
$ django-admin.py startproject --extension=py,.gitignore --template=https://github.com/cirlabs/django-project-template/archive/master.zip project_name
```

Hop into the repo and and install the project dependencies
```bash
$ cd project_name
$ pip install -r requirements.txt
```

## Frontend Setup

:warning: **Make sure you have Node.js installed. If you don't, run** `fab install_node`

If Node.js is installed run:

```bash
$ fab setup
```

You'll be asked if you need to installed the node.js libraries used in this app. If you answer **no**, the installation will be skipped and the front-end generator will run.

See [cirlabs/generator-newsapp](http://github.com/cirlabs/generator-newsapp) to learn how the generator works.

## Check your work

Fire up the server and run grunt tasks:

```bash
$ fab rs
```

## Available Fab commands
```bash
    EC2Connection
    createdb       Creates local database for project
    deploy_static
    deploy_to_s3   Deploy the latest project site media to S3.
    destroy        destoys the database and django project. Be careful!
    dropdb         drops local database for project
    expanduser     Expand ~ and ~user constructions.  If user or $HOME is unk...
    get_node_libs  Install Node.js for Mac OS X or Ubuntu Linux
    grunt          Run grunt tasks installed from Yeoman generator
    gzip_assets    GZips every file in the assets directory and places the ne...
    install_node   Install node.js for Mac OS X or Ubuntu Linux
    production     Work on production environment
    rs             Start development server and grunt tasks
    setup          Fetch required dependencies and setup the front-end
    startapp       Create django app
    yo             Run yeoman generator to scaffold front-end dependencies
```

## Override settings
If you'd like to override the settings in common.py, just create a `local_settings.py` file in `settings/`. `common.py` will import it at the bottom.

## Postgis
In `settings/common.py`:

```python
# POSTGIS
INSTALLED_APPS = (
    ...
    'django.contrib.gis',
}

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '{{ project_name }}',
    }
}
```

## Deployment
We typically deploy the app slug to Heroku and the DB to some DB host (AWS, Rackspace, etc.)

### Procfile
For Heroku, the `Procfile` needs to change to the name of the project. Swap out `project_name` from `web: gunicorn project_name.wsgi` with the name of the project. Read more about Django deploys on Heroku here: [Getting Started with Django on Heroku](https://devcenter.heroku.com/articles/getting-started-with-django)

### Production Database
The `settings/prod.py` file contains all the production-specific variable and settings needed. Configure all your fun there. There's some Heroku-specific stuff in there too if you plan on hosting the database on Heroku as well.

### GeoDjango buildpack
If you're creating a GeoDjango application on Heroku, you're going to need geo spatial libraries like GDAL and PostGIS. Luckily, CIR is here to help.

1. In the project root, create a `.buildpack` file. This tells Heroku that you want to a use a custom buildpack. Buildpacks let you install other necessary libraries and dependecies that your project may need.

2. When creating the Heroku application with the Heroku toolbelt, specify CIR's GeoDjango buildpack. This will ensure the required geo spatial libraries are on your Heroku instance

```bash
$ heroku create --stack cedar --buildpack http://github.com/cirlabs/heroku-buildpack-geodjango/
```

Read more about our GeoDjango buildpack here: [cirlabs/heroku-buildpack-geodjango](https://github.com/cirlabs/heroku-buildpack-geodjango)


Now, get coding you! Remove this `README` file and add your own.

### Credits

This project was inspired by the [@datadesk django-project-template](https://github.com/datadesk/django-project-template)
