#!/usr/bin/python
# -*- coding: utf8 -*-
from django.db import models
from django_countries import CountryField
from pytz import timezone
from django.contrib.auth.models import User
from Ivanhoe.settings import IMAGE_PATH
from django.forms import ModelForm
from Ivanhoe.classification.models import Classification

class Freelancer(models.Model):
    user            = models.ForeignKey(User)
    web_site        = models.URLField(verify_exists=True, max_length=200,default='')
    address         = models.CharField(max_length=200,default='')
    phone           = models.CharField(max_length=20,null=True, default='')
    country         = CountryField(null=True)
    city            = models.CharField(max_length=100,default='')
    time_zone       = timezone('GMT')
    avatar          = models.ImageField(upload_to=IMAGE_PATH,null=True)
    profession      = models.CharField(max_length=100,default='')
    hh_cost         = models.DecimalField(max_digits=10,decimal_places=3, default='0.000')
    bio             = models.CharField(default="",max_length=2000)
        
    def __unicode__(self):
        user = User.objects.get(id=self.user.pk)
        return "ud:%s %s" % (user.id,user.first_name)
    
    
class UserProfile():
    first_name  = ''
    last_name   = ''
    email       = ''
    
    address     = ''
    web_site    = ''
    country     = ''
    city        = ''
    hh_cost     = ''
    phone       = ''
    bio         = ''    
    categories  = []