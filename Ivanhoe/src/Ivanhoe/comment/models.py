#!/usr/bin/python
# -*- coding: utf8 -*-
from django.db import models
from Ivanhoe.job.models import Job
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime

TYPE = (('DM','DM'),('rate','rate'))

class Comment(models.Model):    
    author              = models.ForeignKey(User, null=False)
    to_user             = models.CharField(max_length=100, null=True)
    job                 = models.ForeignKey(Job, null=True)
    text                = models.TextField()
    subject             = models.CharField(max_length=100)    
    datetime            = models.DateTimeField(default=datetime.now, blank=True)
    is_viewed           = models.BooleanField(default=False)
    referenced_comment  = models.CharField(max_length=10, null=True)   
    type                = models.CharField(max_length=20,choices=TYPE,default='DM')
    
    
    
class ViewComment:
    
    def __init__(self,f_id='',f_author='',f_to_user='',f_job='',f_text='',f_subject='',f_datetime='',f_is_viewed=False,job_id=None):
        self.f_id            = f_id
        self.f_author        = f_author
        self.f_to_user       = f_to_user
        self.f_job           = f_job
        self.f_text          = f_text
        self.f_subject       = f_subject    
        self.f_datetime      = f_datetime
        self.f_is_viewed     = f_is_viewed
        
        self.job_id          = job_id
        
    def set_response(self,r_id=None,r_author=None,r_to_user=None,r_job=None,r_text=None,r_subject=None,r_datetime=None,r_is_viewed=None):
        self.r_id            = r_id
        self.r_author        = r_author
        self.r_to_user       = r_to_user
        self.r_job           = r_job
        self.r_text          = r_text
        self.r_subject       = r_subject    
        self.r_datetime      = r_datetime
        self.r_is_viewed     = r_is_viewed