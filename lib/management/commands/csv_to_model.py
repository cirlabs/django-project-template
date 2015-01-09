import csvkit

from django.utils.text import slugify
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = "path/to/file.csv"
    help = "Generate model from CSV"

    def handle(self, *args, **options):
        # read in CSV
        print("This is an auto-generated Django model module \
            created by apps.core.commands.")
        print("from django.contrib.gis.db import models\n")

        with open(args[0], 'rb') as csvfile:

            reader = csvkit.reader(csvfile)
            headers = reader.next()
            print("class GeneratedModel(models.Model):")

            for row in headers:
                # take the row, slugify it
                # and replace the hyphens with underscores
                field = slugify(row).replace('-', '_')
                print("    %s = models.CharField(max_length=255)" % field)

            print("\n")
