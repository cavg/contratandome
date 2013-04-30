from Ivanhoe.feedback.models import Feedback
from Ivanhoe.Util.IvanhoeTest import IvanhoeTest

class SimpleTest(IvanhoeTest):
                                   
    def test_post_feedback_freelancer(self):  
        self.comment = "asdas"
        self.rol     = "freelancer"
              
        response = self.client.post('/post_feedback/', {'comment':self.comment,'rol':self.rol,'email':self.email})    
        f = Feedback.objects.get(user=self.email)
        self.assertEqual(f.comment,self.comment)