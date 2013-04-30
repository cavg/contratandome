#!/usr/bin/python
# -*- coding: utf8 -*-.
from django.contrib.auth.decorators import login_required
from Ivanhoe.shared.views import isFreelancer
from django.shortcuts import render, redirect
from Ivanhoe.job.models import Job
from Ivanhoe.rate.models import Rate
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.models import User
from Ivanhoe.job.views import get_job
from Ivanhoe.comment.models import Comment
from Ivanhoe.Util.Email import Email
from Ivanhoe.Util.Util import message_home
import datetime
from Ivanhoe.job.ViewJob import ViewJob

#TODO: [11 mayo] Rate aspects that was selected celected
 



@require_GET
@login_required
def evaluate(request, code,user):   
     
    try:
        
        is_freelancer,user_rol = isFreelancer(request.user)        
        j = Job.objects.get(code=code)  
        user = User.objects.get(id=j.offer.id)        
        jv = ViewJob()
        jv.to_full_jobView(j)         
                
        if is_freelancer==True:    
            is_rated = jv.is_rated(j.offer)        
            if is_rated:
                return redirect("/job_finish/"+jv.code)
            else:
                return render(request,"evaluate_freelancer.htm", {'job':jv,'isFreelancer':1,'to_user':user})
            
        elif is_freelancer==False:
            is_rated = jv.is_rated(j.assigned.user)                
            if is_rated:
                return redirect("/job_finish/"+jv.code)
            else:
                return render(request,"evaluate_employer.htm", {'job':jv,'isFreelancer':0,'to_user':j.assigned.user}) 
    except Exception,e:
        print e
    return message_home(request)

@require_POST
@login_required
def evaluate_post(request):
    email           = request.POST["email"]
    comment         = request.POST["comment"]
    isFreelancer    = request.POST["isFreelancer"]
    job_id          = request.POST["job_id"]
    user_id         = request.POST["user_id"]
    to_user         = request.POST["to_user"]
    
    job     = Job.objects.get(id=job_id)
    c       =  Comment(author=request.user,to_user=to_user,job=job,text=comment,type='rate')
    c.save()
    
    try:
        msg_text = u"""
            Estimado usuario,<br><br>
            Ya fue evaluado por su contraparte. Para ver su puntáje y comentarios favor acceder a su perfil. <br><br>
            Si usted aun no he calificado le pedimos lo haga a la brevedad.
            <br><br>
            Atte.<br>
            Equipo de desarrollo.<br>contratando ME """ 
        EmailSend = Email()
        EmailSend.send(recipients=[to_user], subject='Contratandome - Usted fue evaluado', message_plaintext=msg_text, message_html=msg_text, default_from_mail='Contratandome <no-reply@contratando.me>')
                    
    except Exception,e:
        print "Exception sending email: %s" % e
        pass
    
    try:
        rates = None
        if isFreelancer=="0":
            rates               = Rate.objects.filter(job=job, user=job.assigned.user)  
        elif isFreelancer=="1":
            rates               = Rate.objects.filter(job=job, user=job.offer)
              
        for r in rates:
            id = "%s" % r.aspect.id
            try:
                Rate.objects.filter(id=r.id).update(score=request.POST[id], evaluation_date=datetime.date.today())
            except Exception,e:
                print "Exception %s" % e    
    except Exception,e:
        print e
    
    #enviar notificación por correo, con link al perfil para ver la nota
            
    return redirect("/job_finish/"+job.code)
    
    
    