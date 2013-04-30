#!/usr/bin/python
# -*- coding: utf8 -*-
from django.db import models
from Ivanhoe.aspect.models import Aspect
from django.contrib.auth.models import User
from Ivanhoe.job.models import Job
from Ivanhoe.employer.models import Employer
from django.utils.datetime_safe import datetime

SCORE       = ((1,1),(2,2),(3,3),(5,5),(8,8),(13,13))

class Rate(models.Model):    
    user            = models.ForeignKey(User)
    aspect          = models.ForeignKey(Aspect)
    job             = models.ForeignKey(Job)
    score           = models.IntegerField(max_length=2, choices=SCORE)
    creation_date   = models.DateField(default=datetime.now, blank=True,null=True)
    evaluation_date = models.DateField(default=datetime.now, blank=True,null=True) 

    def __str__(self):
        return "%s : %d, job: %s" % (self.aspect.name,self.score,self.job.short_description)

class RateView:
    
    def __init__(self,user=None,aspect=None,job=None,score=0,creation_date='',evaluation_date = ''):
        self.user               = user
        self.aspect             = aspect
        self.job                = job
        self.score              = score
        self.creation_date      = creation_date
        self.evaluation_date    = evaluation_date
        
    def __str__(self):
        return "%s : %s" % (self.aspect.name,self.score)