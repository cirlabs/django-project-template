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

