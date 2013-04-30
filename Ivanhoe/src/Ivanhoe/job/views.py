#!/usr/bin/python
# -*- coding: utf8 -*-
from django.shortcuts import render, redirect
from Ivanhoe.job.models import Job
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
import md5
from django.contrib.auth.models import User
from Ivanhoe.classification.models import Classification,META_CATEGORIES
from Ivanhoe.job_classification.models import Job_classification
import logging
import re
from Ivanhoe.freelancer.models import Freelancer
from django.http import HttpResponse
from Ivanhoe.Util.Email import Email
from Ivanhoe.settings import URL
from Ivanhoe.postulate.models import Postulate, ViewPostulate
from Ivanhoe.comment.models import Comment, ViewComment
from Ivanhoe.rate.models import Rate, RateView
from Ivanhoe.Util.Util import message_employer, message_freelancer, message_home
from Ivanhoe.job.ViewJob import ViewJob
from Ivanhoe.shared.Profile import Profile
from Ivanhoe.shared.views import isFreelancer
import datetime
from Ivanhoe.job_classification.views import get_job_classification

logger = logging.getLogger(__name__)

#TODO: Change detail field by cost, time of delivery
#FIXME:[x] accent at select control of categories of services.

def services(request):
    jobs = getServices(limit=4)
    return render(request,'services.htm',{'jobs':jobs})

def services_offered_to_employers(request):
    jobs = getServices(limit=None)
    return render(request,'employer_view_for_services.htm',{'jobs':jobs})

def getServices(limit=3):
    jobs_by_pub = Job.objects.filter(state='1',_type='1').order_by('-publication')
    for j in jobs_by_pub:
        if j.offer==None:
            j.delete()  
    
    if limit==None:
        jobs_by_pub = Job.objects.filter(state='1',_type='1').order_by('-publication')
    else:
        jobs_by_pub = Job.objects.filter(state='1',_type='1').order_by('-publication')[:limit]
     
    jobs = []
    for j in jobs_by_pub:
        jv                = None
        try:
            user                = User.objects.get(username=j.offer)
            offer_name          = "%s %s" % (user.first_name, user.last_name)
            jv = ViewJob(offer_name=offer_name,offer_email=user.email,short_description=j.short_description,extended_description=j.extended_description,budget=j.budget, publication=j.publication, code=j.code, type=j._type)
        except Exception, e:
            logger.error(e)
            print e
        
        try:
            job_c   = Job_classification.objects.filter(job=j)
            jv.classification = []
            for jc in job_c:
                try:
                    cl = Classification.objects.get(id=jc.classification.pk)
                    jv.classification.append(cl.name)
                except Exception,e:
                    print e      
                    logger.error(e)
        except Exception, e:
            print e
            logger.error(e)
        jobs.append(jv)
    return jobs
        

def jobs(request):    
    jobs = getJobs(5)
    return render(request,'jobs.htm',{'jobs':jobs})

#TODO: [27 abril][x] Control for postulate to a job
def jobs_offered_to_freelancers(request):
    jobs = getJobs(None)       
    return render(request,'freelancer_view_for_jobs.htm',{'jobs':jobs,'user':request.user,'allow_comments':True,"categories":META_CATEGORIES})


@require_GET
@login_required
def jobs_offered_to_freelancers_filtered(request):
    classification  = ''
    category        = ''
    price_ini       = 0
    price_end       = 9999999999 
    type_budget     = ''
    try:
        price_ini       = re.sub("\D","","%s" % request.GET["price_ini"])
        price_end       = re.sub("\D","","%s" % request.GET["price_end"])
        type_budget     = request.GET["type_budget"]
        category        = request.GET["category"]
        classification  = request.GET["area"]        
    except Exception,e:
        print e
        
    jobs = list() 
    j_cs = list() 
    
    if category!='0':
        try:
            c = Classification.objects.get(name=classification, category=category)
            j_cs = Job_classification.objects.filter(classification=c)
            #_type       :(('Job','0'),('Service','1'))
            #state       :(('Nulo','-1'),('No Autorizado','0'),('Autorizado','1'),('Terminado','2'))
            #fixed_price : 0 (by hour) | 1 (fixed price) | 2 (both)         
            for jc in j_cs:
                try:
                    if type_budget  == '2':
                        if price_ini=='' and price_end=='':
                            j = Job.objects.get(id=jc.job.pk, _type=0, state=1, fixed_price__range=('0','1'))
                        elif (price_ini!='' and price_end!=''):
                            j = Job.objects.get(id=jc.job.pk, _type=0, state=1, fixed_price__range=('0','1'), budget__range=(price_ini, price_end))
                        else:
                            price_ini = ''
                            price_end = ''
                            j = Job.objects.get(id=jc.job.pk, _type=0, state=1, fixed_price__range=('0','1'))
                    elif type_budget  != '2':
                        if price_ini=='' and price_end=='':
                            j = Job.objects.get(id=jc.job.pk, _type=0, state=1, fixed_price=type_budget)
                        elif (price_ini!='' and price_end!=''):
                            j = Job.objects.get(id=jc.job.pk, _type=0, state=1, fixed_price=type_budget, budget__range=(price_ini, price_end))
                        else:
                            price_ini = ''
                            price_end = ''
                            j = Job.objects.get(id=jc.job.pk, _type=0, state=1, fixed_price=type_budget)         
                    jobs.append(j) 
                except Exception,e:
                    print e
        except Exception,e:
            pass
        
    elif category=='0':
        if type_budget  == '2':
            if price_ini=='' and price_end=='':
                jobs = Job.objects.filter(_type=0, state=1, fixed_price__range=('0','1'))
            elif (price_ini!='' and price_end!=''):                
                jobs = Job.objects.filter(_type=0, state=1, fixed_price__range=('0','1'), budget__range=[price_ini, price_end])
            else:
                price_ini = ''
                price_end = ''
                jobs = Job.objects.filter(_type=0, state=1, fixed_price__range=('0','1'))
        elif type_budget  != '2':
            if price_ini=='' and price_end=='':
                jobs = Job.objects.filter(_type=0, state=1, fixed_price=type_budget)
            elif (price_ini!='' and price_end!=''):
                jobs = Job.objects.filter(_type=0, state=1, fixed_price=type_budget, budget__range=[price_ini, price_end])
            else:
                price_ini = ''
                price_end = ''
                jobs = Job.objects.filter( _type=0, state=1, fixed_price=type_budget)  
    
    
    
    return render(request,'freelancer_view_for_jobs.htm',{'jobs':jobs_to_view(jobs),'user':request.user,'allow_comments':True,"categories":META_CATEGORIES, 'price_ini':price_ini,'price_end':price_end, "category":category,"classification":classification,'type_budget':type_budget})
    

#TODO: [4 mayo][x] As user you can filter the jobs list, using tags, dates and budgets.
def getJobs(limit=3):
    if limit==None:
        js = Job.objects.filter(assigned=None, state=1,_type=0).order_by('-publication')
    else:
        js = Job.objects.filter(assigned=None, state=1,_type=0).order_by('-publication')[:limit]
    return jobs_to_view(js) 
    

def jobs_to_view(js):
    jobs = []
    for j in js:
        jv = ViewJob()
        jv.to_full_jobView(j)
        jobs.append(jv)
    return jobs



#TODO: Define milestones for each project.
#TODO: [4 mayo][x] Wizard for invite freelancer to postulate.
#TODO: [11 mayo] Define aspects to evaluate.
#TODO: [27 abril][x] Choose alternatives of payment: Fixed budget or by hour.
#TODO: [4 mayo][x]  More detail with examples in job form. explaining budgets, details
@login_required
def add_job(request):
    if request.method=='POST':
        try:
            budget                  = request.POST["budget"]        
            budget  = int(re.sub("\D","",budget))
        except Exception,e:
            print e
            budget = 0
        try:
            short_description       = request.POST["short_description"]
            extended_description    = request.POST["extended_description"]
            fixed_price             = request.POST["is_fixed"]
            is_public               = request.POST["is_public"]
            if fixed_price == "0":
                fixed_price = False
            else:
                fixed_price = True
            categories      = request.POST["categories"]
            job = Job(offer=request.user,short_description=short_description, extended_description=extended_description,  budget=budget,fixed_price=fixed_price, public=is_public, state='1')
            job.save()
            code = md5.md5(str(job.id)).hexdigest()
            Job.objects.filter(id=job.id).update(code=code)

            categories_a = categories.split(",")
            for i in categories_a:
                if len(i)>1:
                    c = Classification.objects.get(name=i)   
                    jc = Job_classification(classification=c, job=Job.objects.get(id=job.id))        
                    jc.save()  
            return redirect("/invite_freelancers/"+code)    
        except Exception, e:
            print e
            logger.error(e)        
        return message_employer(request)
    else:        
        return render(request,"add_job_employer.htm", {'categories':META_CATEGORIES}) 
   
                  
#TODO: [27 abril][x] View user postulations, and assigment control    
#TODO: [27 abril][x] Author can close, delete and finish its jobs            
@login_required
def list_my_jobs(request):
    try:
        user = request.user                          
        jobs        = Job.objects.filter(offer=user)
        vjobs       = []
        for j in jobs:
            offer_name          = "%s %s" % (user.first_name, user.last_name)
            jv = ViewJob(offer_name=offer_name,offer_email=user.email,offer_id=user.id,id=j.id, short_description=j.short_description,extended_description=j.extended_description,budget=j.budget, publication=j.publication, code=j.code, type=j._type, assigned=j.assigned)
            vjobs.append(jv)
            
            jv.postulations = list()
            ps  = Postulate.objects.filter(job=j)
            for p in ps:
                vp = ViewPostulate(id=p.id,date=p.date,detail=p.detail,is_accepted=p.is_accepted,job=p.job.id, price=p.price,user=p.user,cause= p.cause, timestamp= p.timestamp)
                jv.postulations.append(vp)
            
            try:
                f_msgs  = Comment.objects.filter(job=j,referenced_comment=None, type='DM')
                jv.comments = list()
                for msg in f_msgs:
                    f_job = "%s" % msg.job.short_description
                    vc    = ViewComment(f_id=msg.id,f_author=msg.author,f_datetime=msg.datetime,f_to_user=msg.to_user,f_job=f_job,f_text=msg.text,f_subject=msg.subject,f_is_viewed=msg.is_viewed,job_id=msg.job.id)       
                    try:
                        r_msg = Comment.objects.get(referenced_comment=msg.id)
                        vc.set_response(r_id=r_msg.id, r_author=r_msg.author, r_to_user=r_msg.to_user , r_job=r_msg.job, r_text=r_msg.text, r_subject=r_msg.subject, r_datetime=r_msg.datetime, r_is_viewed=r_msg.is_viewed)
                    except Exception,e:
                        pass      
                    jv.comments.append(vc) 
            except Exception,e:
                pass
           
        return render(request, 'employer_jobs.htm',{"jobs":vjobs})
    except Exception, e:
        #logger.error(e)
        pass
    return message_employer(request)


def get_job(j,user):
    try:                 
        offer_name          = "%s %s" % (user.first_name, user.last_name)
        jv = ViewJob(offer_name=offer_name,offer_email=user.email,offer_id=user.id,id=j.id, short_description=j.short_description,extended_description=j.extended_description,budget=j.budget, publication=j.publication, code=j.code, type=j._type, assigned=j.assigned,state=j.state)
       
        jv.postulations = list()
        ps  = Postulate.objects.filter(job=j)
        for p in ps:
            vp = ViewPostulate(id=p.id,date=p.date,detail=p.detail,is_accepted=p.is_accepted,job=p.job.id, price=p.price,user=p.user,cause= p.cause, timestamp= p.timestamp)
            jv.postulations.append(vp)
        
        try:
            f_msgs  = Comment.objects.filter(job=j,referenced_comment=None, type='DM')
            jv.comments = list()
            for msg in f_msgs:
                f_job = "%s" % msg.job.short_description
                vc    = ViewComment(f_id=msg.id,f_author=msg.author,f_datetime=msg.datetime,f_to_user=msg.to_user,f_job=f_job,f_text=msg.text,f_subject=msg.subject,f_is_viewed=msg.is_viewed,job_id=msg.job.id)       
                try:
                    r_msg = Comment.objects.get(referenced_comment=msg.id)
                    vc.set_response(r_id=r_msg.id, r_author=r_msg.author, r_to_user=r_msg.to_user , r_job=r_msg.job, r_text=r_msg.text, r_subject=r_msg.subject, r_datetime=r_msg.datetime, r_is_viewed=r_msg.is_viewed)
                except Exception,e:
                    print e        
                jv.comments.append(vc) 
        except Exception,e:
            pass   
        
        # getting aspect to evaluate               
        try:
            rates               = Rate.objects.filter(job=j, user=j.offer)
            if len(rates)>0:
                jv.rates_employer   = []
                for r in rates:
                    rv = RateView(aspect=r.aspect,job=r.job,score=r.score,creation_date=r.creation_date,evaluation_date = r.evaluation_date)
                    jv.rates_employer.append(rv) 
        except Exception,e:
            pass
        try:
            rates               = Rate.objects.filter(job=j, user=j.assigned.user)
            if len(rates)>0:
                jv.rates_freelancer   = []
                for r in rates:
                    rv  = RateView(aspect=r.aspect,job=r.job,score=r.score,creation_date=r.creation_date,evaluation_date = r.evaluation_date)
                    jv.rates_freelancer.append(rv) 
        except Exception,e:
            pass           
    except Exception, e:
        print e                    
    return jv




#job is type Job
@login_required
def redirect_state_job(request,job):
    
    #definicion
    #return add_job(request)

    #invitacion
    #return redirect("/invite_freelancers/"+job.code)
      
    is_freelancer, profile = isFreelancer(request.user)
    jv = ViewJob()
    jv.to_full_jobView(job)
    
    if is_freelancer == False:
        # propuestas y comentarios
        if jv.state=="1" and jv.assigned==None:
            return render(request,"job_employer_postulations.htm", {'j':jv, 'show_link_invite':True})
            
        #define evaluation
        if jv.state=="2" and jv.rates_freelancer==None:
            return redirect("/define_evaluation/"+job.code)
        #contacto
        elif jv.state=="2":
            return redirect("/job_contact/"+job.code)
                
        #proyecto finalizado  
        if jv.state=="3":        
            return render(request,"employer_job_finish.htm", {'j':jv})
        
        #job anulado
        if jv.state=="4" or jv.state=="5" or jv.state=="6":
            return render(request,"job_anulado_employer.htm", {'j':jv})

    elif  is_freelancer == True:              
        #view project not assigned
        if jv.assigned==profile:
            if jv.state=="2" and jv.rates_employer==None:
                return render(request,"freelancer_view_for_job_assigned.htm", {'j':jv,'is_rated':jv.is_rated(request.user)})
                #return redirect("/define_evaluation/"+job.code)
            if jv.state=="2" and jv.rates_employer!=None:
                return redirect("/job_contact/"+job.code)
            is_rated = jv.is_rated(job.offer)
            if jv.state=="3" and is_rated:        
                return redirect("/job_finish/"+jv.code)
            if jv.state=="3" and not is_rated:
                return redirect("/evaluate/"+jv.code+"/"+job.offer.email)
            if jv.state=="4" or jv.state=="5" or jv.state=="6":
                return render(request,"job_anulado_freelancer.htm", {'j':jv})
        else:
            return render(request,'freelancer_view_for_job.htm',{'job':jv,'user':request.user,'allow_comments':True,"categories":META_CATEGORIES})
    
    return message_home(request,"El proyecto aún no se ha activado.")
    # evaluate
    #return redirect("/evaluate/"+job.code+"/"+request.user.email)




##Referente: http://www.bumeran.cl/empleos/capacitadores-freelance-deloitte-1000359481.html
#TODO: [27 abril][x] As freelancer I can ask questions and reply it
@require_GET
def view_job(request, code): 
    try:   
        
        j = Job.objects.get(code=code)  
        user = User.objects.get(id=j.offer.id)
        full_url = request.build_absolute_uri()  
        jc = Job_classification.objects.filter(job=j)
        is_freelancer,user_rol = isFreelancer(request.user)
        
        jv = ViewJob()
        
        if request.user.is_authenticated(): 
            if is_freelancer:
                if j._type == "0":
                    if j.assigned == None:               
                        return redirect_state_job(request, j)
                    else:
                        if request.user==j.assigned.user:
                            return redirect_state_job(request, j)
                        else:
                            return message_freelancer(request, "El trabajo ya fue asignado a otro trabajador.") 
                elif j._type == "1":
                    if request.user==j.offer:
                        job, job_c = get_job_classification(jc,j)
                        return render(request,"view_job.htm", {'job':job,'full_url':full_url,'user':user, 'categories':job_c})
                    elif request.user!=j.offer:                        
                        offer_name          = "%s %s" % (user.first_name, user.last_name)
                        jv = ViewJob(offer_name=offer_name,offer_email=user.email,offer_id=user.id,id=j.id, short_description=j.short_description,extended_description=j.extended_description,budget=j.budget, publication=j.publication, code=j.code, type=j._type, assigned=j.assigned)
                        return render(request,"service.htm", {'j':jv})
            elif not is_freelancer:      
                if j._type == "0":
                    return redirect_state_job(request,j)
                elif j._type == "1":
                    offer_name          = "%s %s" % (user.first_name, user.last_name)
                    jv = ViewJob(offer_name=offer_name,offer_email=user.email,offer_id=user.id,id=j.id, short_description=j.short_description,extended_description=j.extended_description,budget=j.budget, publication=j.publication, code=j.code, type=j._type, assigned=j.assigned)
                    return render(request,"service.htm", {'j':jv})
                
        elif not request.user.is_authenticated():
            if j._type == "0":
                job, job_c = get_job_classification(jc,j)
                return render(request,"view_job.htm", {'job':job,'full_url':full_url,'user':user, 'categories':job_c})
            elif j._type == "1":
                job, job_c = get_job_classification(jc,j)
                return render(request,"view_job.htm", {'job':job,'full_url':full_url,'user':user, 'categories':job_c})
    except Exception,e:
        print e
        
    return message_home(request, "El trabajo no existe")      



@require_GET
@login_required
def finish_job(request, code): 
    try:                   
        j = Job.objects.get(code=code)  
        is_freelancer,user_rol = isFreelancer(request.user)
        jv = ViewJob()
        jv.to_full_jobView(j)        
        
        if is_freelancer==False:
            is_rated = jv.is_rated(j.assigned.user)
            if is_rated:
                e_is_rated = jv.is_rated(j.offer)
                message = None
                if e_is_rated:
                    message = "El proyecto fue finalizado correctamente"
                    Job.objects.filter(id=j.id).update(finish = datetime.datetime.now(), state='3')    
                else:
                    message = "El proyecto sera cerrado una ves que el teletrabajador lo evalué."
                    try:
                        msg_text = u"""
                            Estimado teletrabajador, <br><br>
                            Le recordamos que debe evaluar a su contratante en el proyecto llamado: <br><br>
                            <a href=\"%s\" target='_blank'>%s</a>            
                            <br><br>
                            No olvide que para hacerlo, debe ingresar con su cuenta.<br><br>
                            Atte.<br>
                            Equipo de desarrollo.<br>contratando ME """ % (URL+"/job/"+j.code, j.short_description)  
                        EmailSend = Email()
                        EmailSend.send(recipients=[j.assigned.user.email], subject='Recordatorio de evaluación ContratandoME', message_plaintext=msg_text, message_html=msg_text, default_from_mail='Contratandome <no-reply@contratando.me>')
                    except Exception,e:
                        pass                    
                return render(request,"employer_job_finish.htm", {"j":jv,"message":message})                       
            else:
                return redirect("/evaluate/"+jv.code+"/"+j.assigned.user.email) 
        elif is_freelancer==True:
            message = None
            if jv.state=='3':
                message = "Felicitaciones el proyecto se ha dado por terminado."
            elif jv.state=='2':
                message = "Felicitaciones el proyecto ha sido terminado."
            return render(request,"freelancer_job_finish.htm", {"j":jv,"message":message})   
            
    except Exception,e:
        print e
        
    return message_home(request, "El trabajo no existe")    

@require_GET
def view_job_contact(request, code): 
    try:   
        
        j = Job.objects.get(code=code)  
        user = User.objects.get(id=j.offer.id)
        full_url = request.build_absolute_uri()  
        jc = Job_classification.objects.filter(job=j)
        is_freelancer,user_rol = isFreelancer(request.user)
        
        
        jv = get_job(j, user)   
        if request.user.is_authenticated(): 
            if not is_freelancer:      
                if j._type == "0":
                    if j.state=="2":
                        if jv.rates_freelancer==None:
                            return redirect("/define_evaluation/"+jv.code)
                        else:
                            return render(request,"job_employer_contact.htm", {'j':jv,'is_rated':jv.is_rated(request.user)})  
            else:
                if j._type == "0":
                    if j.state=="2":
                        return render(request,"job_freelancer_contact.htm", {'j':jv,'is_rated':jv.is_rated(request.user)})           
    except Exception,e:
        print e
        
    return message_home(request, "El trabajo no existe")     

@require_GET
def invite_freelancers(request,code):
    try:
        job         = Job.objects.get(code=code)
        #searching job classifications
        jc          = Job_classification.objects.filter(job=job)
        
        freelancers = list()
        for j in jc:
            services    = Job_classification.objects.filter(classification=j.classification)
            for s in services:
                try:
                    service = Job.objects.get(id=s.job.pk,_type=1)
                    profile = Profile(service.offer)
                    freelancer = Freelancer.objects.get(user=service.offer)
                    profile.set_freelancer(freelancer)
                                   
                    js = Job.objects.filter(assigned=freelancer)                    
                    jobs = list()
                    for j in js:
                        jv = ViewJob()
                        jv.to_full_jobView(j)
                        jobs.append(jv) 
                        
                    profile.services = Job.objects.filter(offer=service.offer)
                    profile.calculate_indicators(jobs)
                    
                    
                    #adding just unique freelancers
                    b = True
                    for f in freelancers:
                        if f.freelancer.email == profile.freelancer.email:
                            b = False
                            break
                    if b:
                        freelancers.append(profile)    
                                                                  
                except Exception,e:
                    pass      
                
        if len(freelancers)==0:
            return redirect("/job/"+code)  
        else: 
            return render(request,'invite_freelancers_view_employer.htm',{'job':job,'freelancers':freelancers, 'jcs':jc})        
    except Exception,e:
        print e
        return message_home(request,"Acción no permitida.")


@require_GET
def send_invitation(request,email,code):
    try:
        url = URL+"/job/"+code
        msg_text = u"""
            Estimado teletrabajador, <br><br>
            Ha recibido una invitación para postular al siguiente proyecto.<br><br>
            <a href=\"%s\" target='_blank'>%s</a>            
            <br><br>
            No olvide que para hacerlo, debe ingresar con su cuenta.<br><br>
            Atte.<br>
            Equipo de desarrollo.<br>contratando ME """ % (url, url)  
        EmailSend = Email()
        EmailSend.send(recipients=[email], subject='Le han enviado una oferta de trabajo en ContratandoME', message_plaintext=msg_text, message_html=msg_text, default_from_mail='Contratandome <no-reply@contratando.me>')
    except Exception,e:
        logger.error(e)
    return HttpResponse("ok")  

@require_GET
@login_required
def anular_job(request,code):
    job                     = None
    is_freelancer, profile  = isFreelancer(request.user)
    try:
        job = Job.objects.get(code=code)
        state = '2'
        
        if job.offer==request.user or job.assigned.user==request.user:
            if is_freelancer==True and job.state=='2':
                state = '4'
            if is_freelancer==True and job.state=='5':
                state = '6'
                
            if is_freelancer==False and job.state=='2':
                state = '5'
            if is_freelancer==False and job.state=='4':
                state = '6'
            if state=="6":
                Job.objects.filter(code=code).update(state=state,finish = datetime.datetime.now())
            else:
                Job.objects.filter(code=code).update(state=state)
            return HttpResponse(state)
        else:
            return HttpResponse("-1") 
    except Exception,e:
        print e
    return HttpResponse("-1")    
    
        
@require_GET
@login_required
def delete_job(request, code,rol): 
    try:   
        job = Job.objects.get(code=code,offer=request.user)  
        job.delete()
        if rol=="1":
            return redirect("/dashboard/")
        else:
            return redirect("/add_service/")
    except Exception, e:
        logger.error(e)
    return redirect("/dashboard/")



def add_service(request):  
        
    Jobs = Job.objects.filter(offer=request.user,state=1)
    jobs = []
    for j in Jobs:
        jv                      = None
        try:
            user                = User.objects.get(username=j.offer)
            offer_name          = "%s %s" % (user.first_name, user.last_name)
            jv = ViewJob(offer_name=offer_name,offer_email=user.email,offer_id=user.id,id=j.id, short_description=j.short_description,extended_description=j.extended_description,budget=j.budget, publication=j.publication, code=j.code, type=j._type)
            jv.classification = []
        except Exception, e:
            print e
            logger.error(e)    
        try:
            job_c   = Job_classification.objects.filter(job=j)
            for jc in job_c:
                try:
                    cl = Classification.objects.get(id=jc.classification.pk)
                    jv.classification.append(cl.name)
                except Exception,e:
                    print e      
        except Exception, e:
            print e
        jobs.append(jv)
    
    
    return render(request,'add_job_freelancer.htm',{"categories":META_CATEGORIES,'user_id':request.user.id,'jobs':jobs})
  
  
@login_required
def add_service_post(request):   
    area                    = request.POST["area"]
    name                    = request.POST["name"]
    extended_description    = request.POST["extended_description"]
    offer                   = request.POST["user_id"]
    user                    = User.objects.get(id=offer)    
    
    try:
        job         = Job(offer=user)
        job.save()
        id          = job.id
        code        = md5.md5(str(id)).hexdigest()
    except Exception,e:
        print e
    
    try:
        classification  = Classification.objects.get(name=area)
    except Exception,e:
        print e
        
    try:
        job_c = Job_classification(classification=classification, job=job) 
        job_c.save()
    except Exception,e:
        print e    
    
    try:
        Job.objects.filter(id=id).update(offer=user,short_description=name, extended_description=extended_description,  budget=0, code=code,_type='1',state=1)
    except Exception, e:
        print e
    return add_service(request)








