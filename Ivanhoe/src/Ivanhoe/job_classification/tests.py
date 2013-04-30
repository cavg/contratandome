from Ivanhoe.Util.IvanhoeTest import IvanhoeTest
import md5
from Ivanhoe.job.models import Job
from Ivanhoe.classification.models import Classification
from Ivanhoe.job_classification.models import Job_classification



class SimpleTest(IvanhoeTest):
        
    def test_add_job_classification(self):

        self.job_id                 = "1"
        self.job_name               = "test name"
        self.short_description      = "short description..."
        self.extended_description   = "extended description"
        self.budget                 = 80000
        self.code                   = md5.md5(self.job_id).hexdigest()
        
        job = Job(id=self.job_id, offer=self.user)
        job.save()
                
        self.category   = 'Desarrollo Web'
        self.state      = 'true'
                             
        response = self.client.get('/set_category_job/'+self.category+'/'+self.state+'/'+self.job_id)
        self.assertEqual(response.status_code,200)
        
        c = Classification.objects.get(name=self.category)
        uc = Job_classification.objects.get(job=job)
        self.assertEqual(uc.classification.name,self.category)        
        
        self.state      = 'false'
        response = self.client.get('/set_category_job/'+self.category+'/'+self.state+'/'+self.job_id)
        is_deleted = False
        try:
            uc = Job_classification.objects.get(job=job)
        except Exception,e:
            is_deleted = True
            
        self.assertEqual(is_deleted,True)  
        
        
        