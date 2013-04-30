#!/usr/bin/python
# -*- coding: utf8 -*-
from django.db import models

class File(models.Model):
    filename    = models.CharField(max_length=30)
    file        = models.FilePathField()
    creation    = models.DateTimeField()