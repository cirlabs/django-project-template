<pre><code> ____     _  ____  _      _____ ____               
/  _ \   / |/  _ \/ \  /|/  __//  _ \              
| | \|   | || / \|| |\ ||| |  _| / \|              
| |_/|/\_| || |-||| | \||| |_//| \_/|              
\____/\____/\_/ \|\_/  \|\____\\____/              
                                                   
 ____  ____  ____     _  _____ ____  _____         
/  __\/  __\/  _ \   / |/  __//   _\/__ __\        
|  \/||  \/|| / \|   | ||  \  |  /    / \          
|  __/|    /| \_/|/\_| ||  /_ |  \_   | |          
\_/   \_/\_\\____/\____/\____\\____/  \_/          
                                                   
 _____  _____ _      ____  _     ____  _____  _____
/__ __\/  __// \__/|/  __\/ \   /  _ \/__ __\/  __/
  / \  |  \  | |\/|||  \/|| |   | / \|  / \  |  \  
  | |  |  /_ | |  |||  __/| |_/\| |-||  | |  |  /_ 
  \_/  \____\\_/  \|\_/   \____/\_/ \|  \_/  \____\
                                                   </code></pre>

A custom template for initializing a new Django project. 

Uses the [built-in](https://docs.djangoproject.com/en/1.5/ref/django-admin/#startproject-projectname-destination) Django templating system. Includes a number of small modifications favored the [Los Angeles Times Data Desk](http://datadesk.latimes.com).

Features
--------

* A split of ``settings.py`` that allows for different values in development versus production
* Preinstallation of ``django.contrib.admin``
* Preconfiguration of ``urls.py`` to serve static, media and Munin files
* Preconfiguration of logging options
* Preconfiguration of GeoDjango for PostGIS
* Preinstallation of South migrations
* Preinstallation of django-debug-toolbar
* Fabric functions for local development and production deployment
* Preinstallation of tools for interacting with Amazon Web Services
* Preconfiguration of our preferred caching options

Requirements
------------

* Django
* PostGIS
* Fabric

Getting started
---------------

Create a virtual enviroment to work inside.

```bash
$ virtualenv my-environment
```

Jump in and turn it on.

```bash
$ cd my-environment
$ . bin/activate
```

Install Django.

```bash
$ pip install django
```

Create a new Git repository.

```bash
$ git init repo
```

Download and install a project in there using this template.

```bash
$ django-admin.py startproject --extension=py,.gitignore --template=https://github.com/datadesk/django-project-template/archive/master.zip project repo
```

If your DJANGO_SETTINGS_MODULE is already set you might get an error. If that happens, run the line below and try again.)

```bash
$ export DJANGO_SETTINGS_MODULE=""
$ django-admin.py startproject --extension=py,.gitignore --template=https://github.com/datadesk/django-project-template/archive/master.zip project repo
```

Jump in and install the project's Python dependencies.

```bash
$ cd repo
$ pip install -r requirements.txt
```

Generate a secret key.

```bash
$ fab generate_secret
```

Copy the key. Open the settings file and drop it near the top. While you're there, you can also customize any of the other top level configuration options.

```bash
$ vim project/settings.py
```

Create a PostGIS database to connect with.

```bash
$ createdb -U postgres -E UTF8 -T template_postgis mydatabasename
```

Make a copy of the development settings template.

```bash
$ cp project/settings_dev.template project/settings_dev.py
```

Open it and put in the credentials for the database you just made.

```bash
$ vim project/settings_dev.py
```

Sync the database.

```bash
$ python manage.py syncdb
```

Fire up the test server.

```bash
$ fab rs
```

Get to work. Once you have something worth saving you can replace this README with a description of your new project.
