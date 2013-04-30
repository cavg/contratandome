#!/usr/bin/python
# -*- coding: utf8 -*-
from django.db import models
from Ivanhoe.job.models import Job

STATE = (('No iniciado','No iniciado'),('Iniciado','Iniciado'),('Completado','Completado'))

class Milestone(models.Model):
    job         = models.ForeignKey(Job)
    name        = models.CharField(max_length=100)
    description = models.TextField()
    begin       = models.DateField()
    end         = models.DateField()
    budget      = models.IntegerField()
    state       = models.CharField(max_length=30, choices=STATE)
    