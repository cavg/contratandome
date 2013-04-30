from Ivanhoe.classification.models import Classification
from django.views.decorators.http import require_GET
from Ivanhoe.job.models import Job
from Ivanhoe.job_classification.models import Job_classification
from django.http import HttpResponse


@require_GET
def set_category_job(request,category,state, job_id):   
     
    c = Classification.objects.get(name=category)   
    j = Job.objects.get(id=job_id)     
   
    try:
        if state=="false": 
            uc = Job_classification.objects.get(classification=c, job=j)        
            uc.delete()
         
    except Exception, e:
        pass
    
    try:
        if state=="true": 
            uc = Job_classification(classification=c, job=j)        
            uc.save()         
    except Exception, e:
        pass
            
    
    try:
        r = category+''+state+unicode(request.user)
    except Exception,e:
        pass
    return HttpResponse('<p>'+r+'</p>');

def get_job_classification(jc,j):
    try: 
        job = j         
        job_classifications= []
        for j in jc:
            c = Classification.objects.get(id=j.classification_id)
            job_classifications.append(c.name)
    except Exception,e:
        print e
    return job, job_classifications