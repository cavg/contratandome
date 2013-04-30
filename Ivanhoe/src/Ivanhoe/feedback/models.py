#!/usr/bin/python
# -*- coding: utf8 -*-
from django.db import models
from django.utils.datetime_safe import datetime

class Feedback(models.Model):
    user            = models.CharField(max_length=200,null=True)
    comment         = models.TextField(null=True)
    publication     = models.DateTimeField(default=datetime.now, blank=True)  
        
    def __unicode__(self):
        return self.comment