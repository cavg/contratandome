#!/usr/bin/python
# -*- coding: utf8 -*-
from Ivanhoe.postulate.models import Postulate, ViewPostulate
from django.contrib.auth.models import User
from Ivanhoe.job.models import Job
from django.shortcuts import redirect, render
from Ivanhoe.Util.Email import Email
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse
from Ivanhoe.freelancer.models import Freelancer


@login_required
@require_GET
def set_postulation(request):   
    try:
        id      = request.GET["postulate_id"]
        state   = request.GET["state"]
        cause   = ''
        
        p = Postulate.objects.get(id=id)
        user = User.objects.get(id=p.user.pk)
        email = user.email
        login_url = "http://www.contratando.me/login/" 
        msg_text = u"""
        Estimado, <br><br>
        Ha recibido una respuesta a su postulación. Para revisarla por favor ingrese a su cuenta.<br><br>
        <a href=\"%s\" target='_blank'>%s</a>            
        <br><br>
        Atte.<br>
        Equipo de desarrollo.<br>contratando ME """ % (login_url, login_url)  
        subject = 'Tiene un nuevo mensaje en ContratandoME'
        send_email(email,msg_text,subject)   
        
        if state == "1":
            is_accepted = "1"
            Job.objects.filter(id=p.job.id).update(assigned=Freelancer.objects.get(user=user), state='2')           
            Postulate.objects.filter(id=id).update(is_accepted=1,cause=cause) 
            Postulate.objects.filter(job=p.job).exclude(id=id).update(is_accepted=0) 
        else:
            is_accepted = "0"    
            Postulate.objects.filter(id=id).update(is_accepted=0)         
             
    except Exception, e:
        print e
    return HttpResponse(is_accepted)
   


@login_required
def freelancer_list_postulations(request):
    ps = []
    postulations  = Postulate.objects.filter(user=request.user)
    for p in postulations:
        vp                  = ViewPostulate(date=p.date,detail=p.detail,is_accepted=p.is_accepted,job=p.job.id,job_name=p.job.short_description, price=p.price,user=request.user,cause= p.cause, timestamp= p.timestamp)
        ps.append(vp)    
    return render(request,"freelancer_postulations.htm",{'postulations':ps})

@require_POST
@login_required
def postulate_to_job(request):
    try:
        job         = request.POST["job_id"]
        offer       = request.POST["offer_id"] #who makes the offer to work in        
        price       = request.POST["price"] 
        date        = request.POST["time"]         
        detail      = request.POST["text"]
        
        to          = request.POST["to_id"]    #author's project
                
        co = Postulate(user=User.objects.get(id=offer),job=Job.objects.get(id=job),date=date,detail=detail,price=price)
        co.save()
        
        try:
            user = User.objects.get(id=to)
            email = user.email
            
            login_url = "http://www.contratando.me/login/" 
            msg_text = u"""
            Estimado, <br><br>
            Ha recibido una postulación para su proyecto. Para revisarla por favor ingrese a su cuenta.<br><br>
            <a href=\"%s\" target='_blank'>%s</a>            
            <br><br>
            Atte.<br>
            Equipo de desarrollo.<br>contratando ME """ % (login_url, login_url)  
            subject = 'Tiene un nuevo mensaje en ContratandoME'
            send_email(email,msg_text,subject)  
        except Exception,e:
            print e
        
        return redirect("/jobs_freelancer/")
    except Exception,e:
        print e
    return redirect("/jobs_freelancer/")



def send_email(email_to,msg,subject):
    EmailSend = Email()
    EmailSend.send(recipients=[email_to], subject=subject, message_plaintext=msg, message_html=msg, default_from_mail='Contratandome <no-reply@contratando.me>')

    




