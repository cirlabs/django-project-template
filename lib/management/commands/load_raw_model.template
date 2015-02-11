"""
This management command takes a model created with csv_to_model and provides
code to upload it to a `RawData` model in a new app.

Edit this code with the following:

1. The app name and model name (I like RawData)
2. name of the CSV in the DATA_DIR
3. Match the GeneratedModel attributes to the column headers in the source csv

Finally, save as load_raw_model.py and execute
"""
import os

import csvkit

from django.conf import settings
from django.core.management.base import BaseCommand

from {{ project_name }}.apps.ADD_APP_NAME_HERE.models import RawData

class Command(BaseCommand):
    def handle(self, *args, **options):
        help = "Take model generated with "
        data = os.path.join(settings.DATA_DIR, 'ADD_CSV_NAME_HERE.csv')

        with open(data) as csvfile:

            reader = csvkit.reader(csvfile)
            headers = reader.next()
            count = 0

            for row in reader:
                r = RawData()
                # example
                # r.model_field = row[0]
                # r.another_model_field = row[1]

                try:
                    count += 1
                    r.save()
                    print("Records created: %i ..." % count)
                except Exception, e:
                    raise e
