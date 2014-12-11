# Django Project Template [![Build Status](https://secure.travis-ci.org/cirlabs/django-project-template.png?branch=master)](http://travis-ci.org/cirlabs/django-project-template)

## Requirements
- [Django](https://www.djangoproject.com/)
- [Postgres 9.x](http://www.postgresql.org/)
- [PostGIS 2.0](http://postgis.net/)
- [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/)

## Quickstart
```bash
$ mkvirtualenv project_name
$ pip install django
$ django-admin.py startproject --extension=py,.gitignore --template=https://github.com/cirlabs/django-project-template/archive/master.zip project_name
$ cd project_name
$ pip install -r requirements.txt
```

Need a frontend scaffold too? See [cirlabs/generator-newsapp](http://github.com/cirlabs/generator-newsapp).


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

## Notes
- If you're creating a GeoDjango application on Heroku, you're going to need geo spatial libraries like GDAL and PostGIS. Luckily, CIR is here to help. Read more about our GeoDjango buildpack here: [cirlabs/heroku-buildpack-geodjango](https://github.com/cirlabs/heroku-buildpack-geodjango)
