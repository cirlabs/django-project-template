# Django Project Template [![Build Status](https://secure.travis-ci.org/cirlabs/django-project-template.png?branch=master)](http://travis-ci.org/cirlabs/django-project-template)

## Requirements
- [Django 1.7+](https://www.djangoproject.com/)
- [Postgres 9.3+](http://www.postgresql.org/)
- [PostGIS 2.1+](http://postgis.net/)
- [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/)

## Quickstart
```bash
$ mkvirtualenv project_name
$ pip install django fabric
$ django-admin.py startproject --extension=py,.gitignore --template=https://github.com/cirlabs/django-project-template/archive/master.zip project_name
$ cd project_name
$ fab dev # bootstrap project
```

Need a frontend scaffold too? See [cirlabs/generator-newsapp](http://github.com/cirlabs/generator-newsapp).


## Postgis
By default, this project assumes you'll be using PostGIS as your database. If you'd prefer not to, you can set the `USE_POSTGIS` variable in `settings/common.py` to false and the project will default to PostgreSQL.

## Tasks
```bash
bootstrap     Run commands to setup a new project
build         shortcut for django bakery build command
clear         Remove a model from an application database
compress      shortcut for django compressor offline compression command
createdb      Creates local database for project
deploy_to_s3  Deploy project to S3.
destroy       destoys the database and django project. Be careful!
dropdb        drops local database for project
dumpdata      Dump data of an app in JSON format and store in the fixtures directory
grunt_build   Execute grunt build for any cleanup that needs to happen before deploying.
gzip_assets   GZIP files in the static directory and places files in the gzip directory.
loaddata      load the data of an app in json format
publish       Compress, build and deploy project to Amazon S3
reset         delete all the deploy code
rs            Start development server and grunt tasks. Optionally, specify port
sh            Run Django extensions shell
startapp      Create django app
unbuild       shortcut for django bakery unbuild command

```

## Notes
- If you're creating a GeoDjango application on Heroku, you're going to need geo spatial libraries like GDAL and PostGIS. Luckily, CIR is here to help. Read more about our GeoDjango buildpack here: [cirlabs/heroku-buildpack-geodjango](https://github.com/cirlabs/heroku-buildpack-geodjango)

## Help
Need help? Send a pull request or open an issue in. [ISSUES](https://github.com/cirlabs/django-project-template/issues)

## Contributing
Want to improve the template? Start a new project with the master branch template and add your features/edits. Once you're done, fork the repo, add your changes and send a pull request.

## License

The MIT License (MIT)

Copyright (c) '93 Til ... The Center for Investigative Reporting

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR I
