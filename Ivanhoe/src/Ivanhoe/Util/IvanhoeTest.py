#!/usr/bin/python
# -*- coding: utf8 -*-
from django.test.client import Client
from Ivanhoe.freelancer.models import Freelancer
from Ivanhoe.employer.models import Employer
from django.contrib.auth.models import User
from django.test import TestCase


class IvanhoeTest(TestCase):    
    
    def setUp(self):
        self.client     = Client()        
        self.email      = "cverdugo@alumnos.utalca.cl"
        self.first_name = "Juan"
        self.last_name  = "perez"
        self.password   = "password"
        self.company    = "1024host"
        self.address    = "27 sur 120b"
        self.web_site   = "www.1024host.cl"
        
             
        self.phone      = "96484532"
        self.country    = "AR"
        self.city       = "Talca"
        
        self.user       = User(first_name=self.first_name, email=self.email,username=self.email, last_name=self.last_name)
        self.user.set_password(self.password)
        self.user.save()           
             
        self.client.login(username=self.email, password=self.password)  
        
    def setupFreelancer(self):
        self.freelancer = Freelancer(user=self.user,web_site=self.web_site, address=self.address, phone=self.phone, country=self.country, city=self.city)
        self.freelancer.save()
        
    def setupEmployer(self):
        self.employer = Employer(user=self.user, name=self.company, web_site=self.web_site, address=self.address)
        self.employer.save()