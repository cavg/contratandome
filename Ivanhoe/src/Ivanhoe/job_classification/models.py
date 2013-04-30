#!/usr/bin/python
# -*- coding: utf8 -*-
from django.db import models
from Ivanhoe.classification.models import Classification
from Ivanhoe.job.models import Job

class Job_classification(models.Model):
    classification  = models.ForeignKey(Classification)
    job             = models.ForeignKey(Job)


    def __unicode__(self):
        return "job:%s , classification:%s" % (self.job.short_description,self.classification.name)