from django.core.management.base import BaseCommand
from django.core import management
from django.conf import settings
from django.utils.text import slugify
import csv

class Command(BaseCommand):
  args = "path/to/file.csv"
  help = "Generate model from CSV"

  def handle(self, *args, **options):
    # read in CSV
    print "\n# This is an auto-generated Django model module created by apps.core.commands."
    print "from django.contrib.gis.db import models\n"
    with open(args[0], 'rb') as csvfile:

      reader = csv.reader(csvfile)
      headers = reader.next()
      print "class GeneratedModel(models.Model):"
      for row in headers:
        # take the row, convert to unicode, slugify it, and replace the hyphens with underscores
        field = slugify(unicode(row)).replace('-','_')
        print "    %s = models.CharField(max_length=255)" % field

      print "\n"