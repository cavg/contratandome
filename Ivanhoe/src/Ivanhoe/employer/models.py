#!/usr/bin/python
# -*- coding: utf8 -*-

from django.db import models
from pytz import timezone
from Ivanhoe.settings import IMAGE_PATH
from django_countries import CountryField
from django.contrib.auth.models import User

class Employer(models.Model):
    user            = models.ForeignKey(User)
    name            = models.CharField(max_length=20,null=True)
    web_site        = models.URLField(verify_exists=True, max_length=200,null=True)
    address         = models.CharField(max_length=100,null=True)
    phone1          = models.CharField(max_length=20,null=True)
    phone2          = models.CharField(max_length=20,null=True)
    country         = CountryField(default='CL')
    city            = models.CharField(default="", max_length=50, null=True)
    time_zone       = timezone('GMT')
    avatar          = models.ImageField(upload_to=IMAGE_PATH,null=True)    
        
    def __unicode__(self):
        return self.name+' - '+User.objects.get(id=self.user.id).first_name