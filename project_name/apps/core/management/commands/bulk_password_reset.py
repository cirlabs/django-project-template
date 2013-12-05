from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = "Sets ALL user passwords to the provided arguments. Useful to avoid password leaks"

    def handle(self, *args, **options):
        #frist get used tables
        users = User.objects.all()
        if len(args) < 1:
            print "Requires a password as a argument"
            return
        num_users = User.objects.count()
        print "updating %s users" % num_users
        hashedp = make_password(args[0])
        users.update(password=hashedp)


