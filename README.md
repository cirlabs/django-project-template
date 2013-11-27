# Django Project Template

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

- [Node.js 0.10.x](http://nodejs.org/)
- [npm](http://npmjs.org/) (usually installed with Node)
- [Grunt.js](http://gruntjs.com/getting-started)
- [Bower](http://bower.io/)
- [Yeoman](http://yeoman.io/index.html)

## Kick off

Create virtualenv

```bash
$ mkvirtualenv my-virtual-env
```

Install Django

```bash
$ pip install django
```

Create django project with this template
```bash
$ django-admin.py startproject --extension=py,.gitignore --template=https://github.com/cirlabs/django-project-template/archive/master.zip project
```

Hop into the repo and and install the project dependencies
```bash
$ cd project
$ pip install -r requirements.txt
``` 

## Frontend Setup

:warning: **Make sure you have Node.js installed. If you don't, run** `fab install_node`

If Node.js is installed run:

```bash
$ fab setup
```

You'll be asked if you need to installed the node.js libraries used in this app. If you answer know, the installation will be skipped and the front-end generator will run.

See [cirlabs/generator-newsapp](http://github.com/cirlabs/generator-newsapp) to learn how the generator works.

## Check your work

Phew! Finally, fire up the server to view your setup:

```bash
$ fab rs
```

Now, get coding you! Remove this `README` file and add your own.

### Credits

This project was inspired by the [@datadesk django-project-template](https://github.com/datadesk/django-project-template) 