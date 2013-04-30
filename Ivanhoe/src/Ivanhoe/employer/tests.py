"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
import md5 
from Ivanhoe.employer.models import Employer
from Ivanhoe.job.models import Job
from Ivanhoe.job_classification.models import Job_classification
from Ivanhoe.Util.Email import Email

class Test(TestCase):
    
    def setUp(self):
        self.c          = Client()
        self.email      = 'cverdugo@alumnos.utalca.cl'
        self.first_name = 'Juan'
        self.last_name  = 'perez'
        self.password   = 'password'
        self.company    = '1024host'
        self.address    = '27 sur 120b'
        self.web_site   = 'www.1024host.cl'
        self.u          = User(username=self.email, first_name=self.first_name)    
                     
             
        self.phone      = "96484532"
        self.country    = "AR"
        self.city       = "Talca"
    
    def test_signup(self):
        short_description   = 'Titulo'
        extended_description= 'Descripcion'
        fixed_price         = 1 
        budget              = 90000
        is_public           = 1
        categories          = 'Finanzas'
        name                = 'Camilo Verdugo'
        name1               = 'Camilo'
        name2               = 'Verdugo'
        email               = 'camilo.verdugo@gmail.com'

        response = self.c.post('/signup_employer/',{'short_description':short_description,'extended_description':extended_description,'fixed_price':fixed_price,'is_fixed':'1', 'budget':budget,'is_public':is_public, 'categories':categories, 'name':name,'email':email})        
        self.assertEqual(response.status_code,200)

        user            = User.objects.get(email=email)
        self.assertEqual(user.first_name, name1)
        self.assertEqual(user.last_name, name2)
        
        employer        = Employer.objects.get(user=user) 
        job             = Job.objects.get(short_description=short_description)
        self.assertEqual(job.offer, user)
        self.assertEqual(job.short_description, short_description)
        self.assertEqual(job.extended_description, extended_description)
        uc = Job_classification.objects.get(job=job)
        self.assertEqual(uc.classification.name,categories) 
        
               
    def test_update_account(self):
        
        first_name      = "Andres"
        last_name       = "vergara"
        
        company         = "Contratandome"
        address         = "Santa Isabel 231"
        web_site        = "www.contratando.me"
        phone1          = "96484532"
        phone2          = "02-45678954"       
        country         = "AR"

        u1 = User(first_name=self.first_name, email=self.email,username=self.email, last_name=self.last_name)
        u1.set_password(self.password)
        u1.save()                
        self.c.login(username=u1.username, password=self.password)   
        empl = Employer(user=u1, name=self.company, web_site=self.web_site, address=self.address)
        empl.save()        
                
        response = self.c.post('/update_employer_account_post/', {'employer_id':empl.id,'user_id':u1.id ,'first_name':first_name,'last_name':last_name,'company':company, 'address':address, 'web_site':web_site,'phone1':phone1, 'phone2':phone2, 'country':country})
        self.assertEqual(200, response.status_code) 
        
        u1 = User.objects.get(id=u1.id)
        self.assertEqual(first_name, u1.first_name)
        self.assertEqual(last_name, u1.last_name)
        
        e = Employer.objects.get(id=empl.id)
        self.assertEqual(company, e.name)
        self.assertEqual(web_site, e.web_site)
        self.assertEqual(phone1, e.phone1)
        self.assertEqual(phone2, e.phone2)
        self.assertEqual(country, e.country)
        
    
        

        
