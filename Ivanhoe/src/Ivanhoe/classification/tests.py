from Ivanhoe.job.models import Job
import md5
from Ivanhoe.classification.models import META_CATEGORIES
from Ivanhoe.Util.IvanhoeTest import IvanhoeTest

 
class SimpleTest(IvanhoeTest):
    
        
    def test_get_categories(self):        
        self.job_id                 = "1"
        self.job_name               = "test name"
        self.short_description      = "short description..."
        self.extended_description   = "extended description"
        self.budget                 = 8000099
        self.code                   = md5.md5(self.job_id).hexdigest()
        
        job = Job(id=self.job_id, offer=self.user)
        job.save()
        
        for key,value in META_CATEGORIES:
            response = self.client.get('/categories/'+key)
            self.assertGreater(len(response.content.split(',')),1)       
