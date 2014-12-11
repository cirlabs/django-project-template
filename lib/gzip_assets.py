#!/bin/env python
import os
import gzip
import shutil


class FakeTime:
    def time(self):
        return 1261130520.0

# Hack to override gzip's time implementation
# http://stackoverflow.com/a/264303/868724
gzip.time = FakeTime()

project_dir = '{{ project_name }}'

shutil.rmtree(os.path.join(project_dir, 'gzip'), ignore_errors=True)
shutil.copytree(
    os.path.join(project_dir, 'static'),
    os.path.join(project_dir, 'gzip/static')
)

for path, dirs, files in os.walk(os.path.join(project_dir, 'gzip/static')):
    for filename in files:
        file_path = os.path.join(path, filename)

        f_in = open(file_path, 'rb')
        contents = f_in.readlines()
        f_in.close()
        f_out = gzip.open(file_path, 'wb')
        f_out.writelines(contents)
        f_out.close()
