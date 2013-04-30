#!/usr/bin/python
# -*- coding: utf8 -*-
from django.db import models
from django.contrib.auth.models import User
from Ivanhoe.freelancer.models import Freelancer
from django.utils.datetime_safe import datetime

#-1 nulo, 0 no autorizado, 1 autorizado, 2 en curso, 3 terminado, 4 anulado freelancer, 5 por employer, 6 anulado por ambos
STATE           = (('-1','-1'),('0','0'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'))
TYPE            = (('Job','0'),('Service','1'))

class Job(models.Model):
    offer               = models.ForeignKey(User, null=True)
    assigned            = models.ForeignKey(Freelancer, null=True)
    short_description   = models.TextField(null=True,blank=True)
    extended_description= models.TextField(null=True)
    budget              = models.IntegerField(default=0, max_length=20)
    publication         = models.DateTimeField(default=datetime.now, blank=True)
    finish              = models.DateTimeField(default=datetime.now)
    state               = models.CharField(max_length=30, choices=STATE, null=True, default=-1)
    code                = models.CharField(max_length=128, null=True)
    _type               = models.CharField(max_length=20, choices=TYPE, default=0)
    fixed_price         = models.BooleanField(default=True)
    public              = models.BooleanField(default=False)
    
    def __unicode__(self):
        if self.short_description!=None:
            return "(%s) %s" % (self.pk,self.short_description)
        else:
            return str(self.pk)
    
        

