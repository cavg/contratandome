# -*- coding: utf8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from Ivanhoe.freelancer.models import Freelancer
from Ivanhoe.freelancer.views import get_freelancers
from Ivanhoe.user_classification.models import User_classification
from Ivanhoe.classification.models import META_CATEGORIES, Classification

class SimpleTest(TestCase):
    
    def setUp(self):
        self.c          = Client()
        self.email      = 'camilo.verdugo@gmail.com'
        self.first_name = 'Juan'
        self.last_name  = 'perez'
        self.password   = 'password'
        self.web_site   = 'www.cverdugo.1024host.cl'
        self.address    = "Santa Isabel 231"
        self.phone      = "96484532"
        self.country    = "AR"
        self.city       = "Talca"
    
    #signup_freelancer
    def test_add_user(self):
        response = self.c.post('/signup_freelancer_post/', {'first_name':self.first_name,'last_name':self.last_name,'email':self.email, 'password':self.password,'repassword:':self.password})
                   
        u = User.objects.get(email=self.email)
        self.assertEqual(u.first_name, self.first_name)
        f = Freelancer.objects.get(user=u.pk)
        self.assertEqual(u.id,f.user_id)
    
        
    def test_update_account(self):
        
        city        = "Curicó" 
        hh_cost     = 9500.000    
        web_site    = "www.google.com"
        phone       = '91234567'
        country     = "CL"
        address     = "Avenida Alexandri #542"
        bio         = "blabla"
         

        u1 = User(first_name=self.first_name, email=self.email,username=self.email, last_name=self.last_name)
        u1.set_password(self.password)
        u1.save()                
        self.c.login(username=u1.username, password=self.password)   
        free = Freelancer(user=u1,web_site=self.web_site, address=self.address, phone=self.phone, country=self.country, city=self.city)
        free.save()        
                
        response = self.c.post('/update_freelancer_account_post/', {'freelancer_id':free.id,'city':city ,'user_id':u1.id,'hh_cost':hh_cost,'web_site':web_site, 'address':address, 'phone':phone,'country':country, 'bio':bio})
        self.assertEqual(200, response.status_code) 
        
               
        f = Freelancer.objects.get(id=free.id)
#        self.assertEqual(city.decode('utf-8'), f.city.decode('utf-8'))
        self.assertEqual(hh_cost, f.hh_cost)
        self.assertEqual(web_site, f.web_site)
        self.assertEqual(phone, f.phone)
        self.assertEqual(country, f.country)
        self.assertEqual(address, f.address)
        self.assertEqual(bio, f.bio)
        
    def test_get_freelancers(self):
        bio         = "blabla"
        u1 = User(first_name=self.first_name, email=self.email,username=self.email, last_name=self.last_name)
        u1.set_password(self.password)
        u1.save()                
        self.c.login(username=u1.username, password=self.password)   
        free = Freelancer(user=u1,web_site=self.web_site, address=self.address, phone=self.phone, country=self.country, city=self.city, bio=bio)
        free.save()  
        
        cat_name = "Programming"
        clas    = Classification(name=cat_name, category=META_CATEGORIES[0])
        clas.save()
        usercat = User_classification(user=u1, classification=clas)
        usercat.save() 
        
        
        freelancers = get_freelancers()
        self.assertEqual(len(freelancers),1)
        self.assertEqual(freelancers[0].address,self.address)
        self.assertEqual(freelancers[0].country,self.country)
        self.assertEqual(freelancers[0].city,self.city)
        self.assertEqual(freelancers[0].phone,self.phone)
        self.assertEqual(freelancers[0].bio,bio)
        self.assertEqual(freelancers[0].first_name,self.first_name)
        self.assertEqual(freelancers[0].last_name,self.last_name)
        self.assertEqual(freelancers[0].email,self.email)
        self.assertEqual(freelancers[0].categories[0],cat_name)
        
        
        
        