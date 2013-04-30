from Ivanhoe.job.models import Job
from Ivanhoe.classification.models import Classification
import md5
from Ivanhoe.Util.IvanhoeTest import IvanhoeTest
from Ivanhoe.job_classification.models import Job_classification
from Ivanhoe.freelancer.models import Freelancer
from django.contrib.auth.models import User

class SimpleTest(IvanhoeTest):  
                
    def test_add_job(self):      
        self.job_id                 = "1"
        self.short_description      = "short description..."
        self.extended_description   = "extended description"
        self.budget                 = 980000
        self.code                   = md5.md5(self.job_id).hexdigest()
        self.is_canceled            = "0"
        self.is_fixed               = "1"
        self.is_public              = "1"
        self.categories             = "Logos,Banner"

        response = self.client.post('/add_job/',{'categories':self.categories,'is_public':self.is_public,'is_canceled':'0','short_description':self.short_description,'extended_description':self.extended_description,'budget':self.budget,'is_fixed':self.is_fixed,'is_canceled':self.is_canceled})
        #self.assertEqual(response.status_code,200)

        job = Job.objects.get(short_description = self.short_description) 
        self.assertEqual(job.extended_description,self.extended_description)
        self.assertEqual(job.budget,self.budget)
        
        
    def test_list_my_jobs(self):
      
        self.job_id                 = "1"
        self.job_name               = "test name"
        self.short_description      = "short description..."
        self.extended_description   = "extended description"
        self.budget                 = 80000
        self.code                   = md5.md5(self.job_id).hexdigest()
        
        job = Job(id=self.job_id,short_description=self.short_description, offer=self.user)
        job.save()
        response = self.client.get('/list_my_jobs/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.context['jobs']),1)
        self.assertEqual(response.context['jobs'][0].short_description,self.short_description)
        
    def test_invite_freelancer(self):
        
        self.job_id     = "2"
        self.job_name   = "nombre"
        self.code       = md5.md5(self.job_id).hexdigest()
        
        job = Job(id=self.job_id,offer=self.user, code=self.code)
        job.save()
        c   = Classification.objects.get(id=1)  
        jc  = Job_classification(job=job,classification=c) 
        jc.save()
        
        
        email = "bill_gates@gmail.com"
        u2    = User(first_name=self.first_name, email=email,username=email, last_name=self.last_name)
        u2.set_password(self.password)
        u2.save()           
        
        freelancer = Freelancer(user=u2,web_site=self.web_site, address=self.address, phone=self.phone, country=self.country, city=self.city)
        freelancer.save()
        
        s_id = '3'
        service = Job(id=s_id, offer=u2,_type='1',state=1,code=md5.md5(s_id).hexdigest())
        service.save()
        
        job_s = Job_classification(classification=c, job=service) 
        job_s.save()
        
        response = self.client.get('/invite_freelancers/'+self.code)
        self.assertEqual(len(response.context['freelancers']),1)
             
    
    