#!/usr/bin/python
# -*- coding: utf8 -*-
from django.db import models
from django.contrib.auth.models import User
from Ivanhoe.job.models import Job
from django.utils.datetime_safe import datetime

OPTIONS = (('-1','-1'),('0','0'),('1','1'))

class Postulate(models.Model):
    user            = models.ForeignKey(User)  
    job             = models.ForeignKey(Job)
    is_accepted     = models.CharField(default='-1',max_length=2, choices= OPTIONS)
    date            = models.CharField(max_length=3,default='')
    price           = models.CharField(max_length=10,default='')
    detail          = models.CharField(max_length=2000,default='')
    cause           = models.CharField(max_length=2000,default='')
    timestamp       = models.DateTimeField(default=datetime.now) 
    
    def __unicode__(self):
        return "(%s) job:%s" % (self.id,self.job.short_description)
    
class ViewPostulate:
    
    def __init__(self,id='',user='',job='',job_name='',is_accepted=None,date='',price='',detail='',cause='',timestamp=''):
        self.id              = id
        self.user            = user
        self.job             = job
        self.job_name        = job_name 
        self.is_accepted     = is_accepted
        self.date            = date
        self.price           = price
        self.detail          = detail
        self.cause           = cause
        self.timestamp       = timestamp  