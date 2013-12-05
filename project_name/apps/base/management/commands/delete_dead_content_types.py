from django.core.management.base import BaseCommand
from django.db.models import get_apps, get_models

from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = "finds unused content types in the database and kills them"

    def handle(self, *args, **options):
        #frist get used tables

        installed_apps = set()
        apps = get_apps()
        for app in apps:
            models = get_models(app)
            if(models):
                installed_apps.add(models[0]._meta.app_label)

        ct_apps = set()
        for ct in ContentType.objects.all():
            ct_apps.add(ct.app_label)

        ct_list = ct_apps.difference(installed_apps)

        for ct_label in ct_list:
            for ct in ContentType.objects.filter(app_label=ct_label):
                ct.delete()
