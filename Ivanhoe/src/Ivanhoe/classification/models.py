#!/usr/bin/python
# -*- coding: utf8 -*-
from django.db import models

META_CATEGORIES = [('Computacion e Informatica','Computación e Informática'),
                   ('Diseno','Diseño'),('Escrituras','Escrituras'),
                   ('Marketing y Ventas','Marketing y Ventas'),
                   ('Administracion','Administración'),
                   ('Consultorias','Consultorías'),
                   ('Legal','Legal'),
                   ('Ingenieria','Ingeniería')] 

class Classification(models.Model):
    name        = models.CharField(max_length=100)
    category    = models.CharField(max_length=100, choices=META_CATEGORIES)   


    def __unicode__(self):
        return "%s - %s" % (self.category,self.name)