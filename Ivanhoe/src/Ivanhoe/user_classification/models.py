# -*- coding: utf8 -*-
from django.db import models
from Ivanhoe.classification.models import Classification
from django.contrib.auth.models import User

class User_classification(models.Model):  
    classification  = models.ForeignKey(Classification)
    user            = models.ForeignKey(User)
    