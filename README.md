
A custom template for initializing a new Django project that includes a number of small modifications favored the [Los Angeles Times Data Desk](http://datadesk.latimes.com).

Features
--------

* A split of ``settings.py`` that allows for different values in development versus production
* Preinstallation of ``django.contrib.admin``
* Preconfiguration of ``urls.py`` to serve static, media and Munin files
* Preconfiguration of logging options
* Preconfiguration of GeoDjango for PostGIS
* Preinstallation of South migrations
* Preinstallation of django-debug-toolbar
* A ``fabfile.py`` that includes a variety of Fabric functions
* Preinstallation of tools for interacting with Amazon Web Services
* Preconfiguration of our preferred caching options

Getting started
---------------

```bash
$ django-admin.py startproject --extension=py,.gitignore --template=https://github.com/datadesk/django-project-template/archive/master.zip project
```
