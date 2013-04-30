# Create your views here.
from django.contrib.auth.decorators import login_required
from Ivanhoe.shared.views import isFreelancer
from django.http import HttpResponse
from django.shortcuts import render, redirect
from Ivanhoe.aspect.models import Aspect
from Ivanhoe.job.models import Job
from Ivanhoe.job_classification.models import Job_classification
from django.views.decorators.http import require_GET
from Ivanhoe.rate.models import Rate
from Ivanhoe.freelancer.models import Freelancer
from django.contrib.auth.models import User

#TODO: [11 mayo] List evaluation aspects for each category of job and service
#TODO: [11 mayo] Select a aspect for each job

@login_required
def define_evaluation(request,code):
    user                    = request.user
    is_freelancer, profile  = isFreelancer(user)
    job                     = Job.objects.get(code=code)
    
    jc              = Job_classification.objects.filter(job=job)
    classifications = list()
    for c in jc:
        classifications.append(c.classification.category)
    classifications = set(classifications)
    saspects        = list()
    for c in classifications:
        a = Aspect.objects.filter(classification=c)
        for ai in a:
            saspects.append(ai)
        
    if is_freelancer:
        rates =  Rate.objects.filter(user=job.offer,job=job)      
        if len(rates)>0:
            return redirect("/job_contact/"+job.code)
        else:
            gaspects         = Aspect.objects.filter(type="General",user="Empresa")
            
            #setting up general aspect
            for g in gaspects:
                r = Rate(user=job.offer,aspect=g,job=job,score=0)
                r.save()
                
            return render(request,"define_evaluation_freelancer.htm",{'gaspects':gaspects,'job':job})     
            
    else:
        gaspects         = Aspect.objects.filter(type="General", user="Freelancer") 
        #setting up general aspect
        for g in gaspects:
            r = Rate(user=job.assigned.user,aspect=g,job=job,score=0)
            r.save()       
        return render(request,"define_evaluation_employer.htm",{'gaspects':gaspects,'saspects':saspects,'job':job})
    
    return HttpResponse("test")

@require_GET
def set_aspect(request,code,id,state,user):
    job = Job.objects.get(code=code)
    a   = Aspect.objects.get(id=id)    
    print state
    if state =="1":
        r = Rate(user=User.objects.get(id=user),aspect=a,job=job,score=0)#creation_date=,evaluation_date=   
        r.save()
        pass
    else:
        r = Rate.objects.filter(aspect=a,job=job)
        r.delete()
        pass
        
    return HttpResponse("")













