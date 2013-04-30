from Ivanhoe.employer.models import Employer
from Ivanhoe.freelancer.models import Freelancer
from Ivanhoe.job.models import Job
from Ivanhoe.job_classification.models import Job_classification
from django.test import TestCase
from django.contrib.auth.models import User
import md5 
from django.test.utils import setup_test_environment
from django.test.client import Client
setup_test_environment()


class SimpleTest(TestCase):
    
    def setUp(self):
        self.c          = Client()
        self.email      = 'juanito@gmail.com'
        self.first_name = 'Juan'
        self.last_name  = 'perez'
        self.password   = 'password'
        self.company    = '1024host'
        self.address    = '27 sur 120b'
        self.web_site   = 'www.1024host.cl'
    
    def test_activate_freelancer(self):
        u = User(first_name=self.first_name, last_name=self.last_name,email=self.email, is_active=False)
        u.save()
        u = User.objects.get(email=self.email)
        self.assertEqual(u.is_active,False)
        response = self.c.get('/activation/'+self.email+'/'+md5.md5(self.email+self.last_name).hexdigest())        
        u = User.objects.get(email=self.email)       
        self.assertEqual(u.is_active,True) 

    def test_singup_employer(self):
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

        

        #add job, user, employer, category
        #check password, url activation



        
    def test_check_session(self):
        u = User(first_name=self.first_name, last_name=self.last_name,email=self.email,username=self.email, is_active=True)
        u.set_password(self.password)
        u.save()
        self.assertEqual(self.c.login(username=self.email, password=self.password), True)
        self.c.logout()           
        
    #login
    def test_check_user(self):
        u = User(first_name=self.first_name, last_name=self.last_name,email=self.email)
        u.save()
        response = self.c.get('/check_user/'+self.email)
        self.assertEqual(response.content,"1")
        
        email2 = 'juan2@gmail.com'
        response = self.c.get('/check_user/'+email2)
        self.assertEqual(response.content,"0")
        
    #profile    
    def test_profile(self):
      
        u = User(first_name=self.first_name, last_name=self.last_name,email=self.email)
        u.save()        
        empl = Employer(user=u, name=self.company, web_site=self.web_site, address=self.address)
        empl.save()         
        
        response = self.client.get('/profile/'+self.email)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['profile'].user.first_name, self.first_name)
        self.assertEqual(response.context['profile'].user.last_name, self.last_name)
        self.assertEqual(response.context['profile'].user.email,self.email)  
              
        if response.context['isFreelancer'] == False:
            self.assertEqual(response.context['profile'].employer.name,self.company)
            self.assertEqual(response.context['profile'].employer.web_site,self.web_site) 
            self.assertEqual(response.context['profile'].employer.address,self.address)   
        
        
       
        empl.delete()
        free = Freelancer(user=u,web_site=self.web_site, address=self.address)
        free.save()    
                
        response = self.client.get('/profile/'+self.email)
        
        if response.context['isFreelancer'] == True:
            self.assertEqual(response.context['profile'].freelancer.web_site,self.web_site) 
            self.assertEqual(response.context['profile'].freelancer.address,self.address)   
            
        print response.context['jobs']
        
        
        
        
        
        
        
        
