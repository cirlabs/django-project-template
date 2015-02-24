# Django Project Template [![Build Status](https://secure.travis-ci.org/cirlabs/django-project-template.png?branch=master)](http://travis-ci.org/cirlabs/django-project-template)

Django Project Template is a collection of development tasks and optimizations aimed at anyone doing news application development on tight deadlines in Django. Highlights include:

- [PostGIS](http://postgis.net/) setup for geospatial database work
- [Fabric](http://www.fabfile.org/) tasks for development, building and deployment
- Preconfigured with [Django Compressor](http://django-compressor.readthedocs.org/en/latest/) for CSS and JS preprocessing, concatenation and minification
- Preconfigured deploy chain for baking projects flat with [Django Bakery](http://django-bakery.readthedocs.org/en/latest/)
- [Boto](http://docs.pythonboto.org/en/latest/) configuration for easy deployment to [Amazon S3](https://aws.amazon.com/s3/)
- Works with our custom built [yeoman generator](https://github.com/cirlabs/generator-newsapp) for even faster front-end scaffolding, development and optimization with [Grunt](http://gruntjs.com/) and [Bower](http://bower.io/)

## Minimum Requirements
This project supports Ubuntu Linux 14.04 and Mac OS X Yosemite. It is not tested or supported for the Windows OS.

- [Django 1.7+](https://www.djangoproject.com/)
- [PostgreSQL 9.3+](http://www.postgresql.org/)
- [PostGIS 2.1+](http://postgis.net/)
- [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/)
- *OPTIONAL:* [Node.js 0.12.x](http://nodejs.org/) or [io.js 1.2.x](https://iojs.org/en/index.html)

## Quickstart
```bash
$ mkvirtualenv project_name
$ pip install django fabric
$ django-admin.py startproject --extension=py,.gitignore --template=https://github.com/cirlabs/django-project-template/archive/master.zip project_name
$ cd project_name
$ fab bootstrap # bootstrap project
```

## Deployment
This project assumes you have an Amazon S3 bucket where you host your apps. They are static apps with no database calls.

Update `settings/production.py` with the various s3 buckets you'll use. We have buckets for staging (testing the application), buckets for media assets and a final bucket publishing. You can use these conventions or change them. You'll also need to add the [Django Bakery views](http://django-bakery.readthedocs.org/en/latest/gettingstarted.html#configuration) you want generated.

You'll also need to create a `settings/local_settings.py` file with your AWS secret key and ID. By default this file __will not__ be checked into version control. Keep it that way just in case your open source your project. This ensures you keys won't leak out to the world.

With those files configured, run `fab deploy` to publish your application to the world.

#### On Database-powered applications
You can certainly use this template for dynamic applications, but currently there is no deployment chain.

### Using Yeoman, Grunt and Bower (recommended)
While this template works fine out the box, it's recommended you use use our yeoman generator to manage your static assets (HTML, CSS, JS). We built [generator-newsapp](https://github.com/cirlabs/generator-newsapp) to work in concert with this project template. For this to work you'll need [Node.js 0.12.x](http://nodejs.org/) or [io.js 1.2.x](https://iojs.org/).

After running the quick start above run `fab scaffold` to install the required node.js libraries and generate the templates needed for frontend development.

### PostGIS
By default, this project assumes you'll be using PostGIS as your database. If you'd prefer not to, you can set the `USE_POSTGIS` variable in `settings/common.py` to `False` and the project will default to PostgreSQL. :warning: Be sure to do this BEFORE running the quickstart.

### Tasks
Here are the various fabric tasks included in the project. See [fabfile.org](http://fabfile.org) to learn more about Fabric and Python task execution.

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

### A note about GeoDjango deployment on Heroku
- If you're creating a GeoDjango application on Heroku, you're going to need geospatial libraries like GDAL and PostGIS. Luckily, CIR is here to help. Read more about our GeoDjango buildpack here: [cirlabs/heroku-buildpack-geodjango](https://github.com/cirlabs/heroku-buildpack-geodjango)

### Help
Need help? Open an issue in: [ISSUES](https://github.com/cirlabs/django-project-template/issues)

### Contributing
Want to improve the template? Fork the repo, add your changes and send a pull request.

### Thanks
Special thanks goes to Chase Davis for his initial work at developing our Django template for CIR. Also, this project's structure borrows many great ideas from Ben Welsh at the Los Angeles Times Datadesk and his [Django Project Template](https://github.com/datadesk/django-project-template).

### License
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
