from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import get_apps, get_models


class Command(BaseCommand):
    help = "finds unused tables in the database"
    args = 'output type'

    def handle(self, *args, **options):
        #frist get used tables

        tables = connection.introspection.table_names()
        used_tables = []
        for app in get_apps():
            for model in get_models(app, include_auto_created=True):
                used_tables.append(model._meta.db_table)
        unused = list(set(tables) - set(used_tables))
        if 'sql' in args:
            print 'SET FOREIGN_KEY_CHECKS=0; drop table',
            format = "%s,\n"
        else:
            print 'excess tables:'
            format = "\t%s\n"
        #print all but the last one
        for table in unused[:-1]:
            print format % table,
        if 'sql' in args:
            print '%s;' % unused[-1]
            print 'SET FOREIGN_KEY_CHECKS=1;'
