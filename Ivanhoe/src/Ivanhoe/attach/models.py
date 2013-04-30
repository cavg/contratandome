#!/usr/bin/python
# -*- coding: utf8 -*-
from django.db import models
from Ivanhoe.job.models import Job
from Ivanhoe.file.models import File

class Attach(models.Model):
    job     = models.ForeignKey(Job)
    file    = models.ForeignKey(File)
