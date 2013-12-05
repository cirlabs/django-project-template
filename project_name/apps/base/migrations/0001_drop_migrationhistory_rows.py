# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        db.execute("delete from south_migrationhistory where id=147;")
        db.execute("delete from south_migrationhistory where id=148;")
        db.execute("delete from south_migrationhistory where id=162;")
        db.execute("delete from south_migrationhistory where id=192;")

        db.execute("drop table donations_directmaildonation;")
        db.execute("drop table donations_directmaildonation_giftoptions;")
        db.execute("drop table donations_donation;")
        db.execute("drop table donations_donation_giftoptions;")
        db.execute("drop table donations_donortestimonial;")
        db.execute("drop table donations_gift;")
        db.execute("drop table donations_gift_images;")
        db.execute("drop table donations_gift_option_sets;")
        db.execute("drop table donations_giftdonation;")
        db.execute("drop table donations_giftdonation_giftoptions;")
        db.execute("drop table donations_giftoption;")
        db.execute("drop table donations_giftoptionset;")
        db.execute("drop table donations_giftoptionset_options;")
        db.execute("drop table donations_giftset;")
        db.execute("drop table donations_giftset_gifts;")
        db.execute("drop table donations_grassrootdonation;")
        db.execute("drop table donations_grassrootdonation_giftoptions;")
        db.execute("drop table donations_grassrootsubscription;")
        db.execute("drop table donations_grassrootsubscription_giftoptions;")
        db.execute("drop table donations_referral;")
        db.execute("drop table donations_subscription;")
        db.execute("drop table donations_subscription_giftoptions;")


    def backwards(self, orm):
        pass

    models = {

    }

    complete_apps = ['base']
    symmetrical = True



