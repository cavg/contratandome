# -*- coding: utf8 -*-
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
import md5
from Ivanhoe.freelancer.models import Freelancer
from Ivanhoe.employer.models import Employer
from Ivanhoe.classification.models import Classification, META_CATEGORIES
from Ivanhoe.freelancer.views import update_account_freelancer
from Ivanhoe.job_classification.models import Job_classification
from Ivanhoe.user_classification.models import User_classification
from Ivanhoe.job.models import Job
import logging
from Ivanhoe.employer.views import update_account_employer
from Ivanhoe.rate.models import Rate
from Ivanhoe.Util.Util import message_home
from Ivanhoe.job.ViewJob import ViewJob
from Ivanhoe.shared.Profile import Profile
logger = logging.getLogger(__name__)


#TODO: FAQS section with moderation.

@require_GET
def profile(request,email):
    try:
        user    = User.objects.get(email=email)
        profile = None
        jobs    = None
        is_freelancer,user_rol = isFreelancer(user)
        
        profile = Profile(user)
        try:
            if is_freelancer == True:
                js = Job.objects.filter(assigned=user_rol)
                profile.set_freelancer(user_rol)
            else:
                js = Job.objects.filter(offer=user)
                profile.set_employer(user_rol)
                
            jobs = list()
            for j in js:
                jv = ViewJob()
                jv.to_full_jobView(j)
                jobs.append(jv) 
                
            profile.calculate_indicators(jobs)            
        except Exception,e:
            pass
        
        services = None
        if is_freelancer == True:
            jser = Job.objects.filter(offer=user, _type="1")
            services = list() 
            for j in jser:
                jv = ViewJob()
                jv.to_full_jobView(j)
                services.append(jv)
        return render(request,'profile.htm',{'profile':profile,'isFreelancer':is_freelancer,'jobs':jobs,'services':services})
    except Exception,e:
        print e
        
    return message_home(request,"Usuario inválido.")
    


@login_required
def update_account(request):
    user = request.user    
    try:
        freelancer  = Freelancer.objects.get(user=user.pk)
        return update_account_freelancer(request)
    except Exception, e:
        pass
    try:
        employer = Employer.objects.get(user=user.pk)
        return update_account_employer(request)
    except Exception,e:
        pass
    return message_home(request)

@login_required
def change_password(request):
    return render(request, 'change_password.htm')

#TODO: As Freelancer and contractor I can change/reset my password account.

@require_POST
def check_login(request):
    try:
        email   = request.POST['username']
        password= request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:               
                login(request,user)     
                return redirect('/dashboard/')    
            else:
                return _login(request, message="Credencial inválida, active su cuenta o por favor póngase en contacto con el equipo de soporte <soporte@contratando.me>.")  
        else:
            return _login(request, message="La contraseña no es válida. Por favor, asegúrate de que la el bloqueo de mayúsculas no está activado e inténtalo de nuevo.")
    except Exception, e:
        print e 
    return message_home(request)

@login_required
def dashboard(request, message=None):    
    user = request.user            
    is_freelancer,profile = isFreelancer(user)
    if is_freelancer:
        try:
            js  = Job.objects.filter(assigned=Freelancer.objects.get(user=user)).order_by('-publication')
            
            jobs  = []
            for j in js:
                jv = ViewJob(id=j.id,short_description=j.short_description,extended_description=j.extended_description,publication=j.publication,code=j.code,state=j.state)
                try:
                    rates               = Rate.objects.filter(job=j, user=j.offer)
                    if len(rates)>0:
                        jv.rates_employer   = []
                        jv.rates_employer.append(rates) 
                except Exception,e:
                    pass
                jobs.append(jv)
            
            return render(request, 'dashboard_freelancer.htm',{'email':user.username,'jobs': jobs ,'message':message})    
        except Exception, e:
            pass
    else:
        try:
            js      = Job.objects.filter(offer=user).order_by('-publication')
            jobs    = []
            for j in js:
                jv = ViewJob(id=j.id,short_description=j.short_description,extended_description=j.extended_description,publication=j.publication,code=j.code,state=j.state)
                try:
                    rates               = Rate.objects.filter(job=j, user=j.assigned.user)
                    if len(rates)>0:
                        jv.rates_employer   = []
                        jv.rates_employer.append(rates) 
                except Exception,e:
                    pass
                jobs.append(jv)         
            return render(request, 'dashboard_employer.htm',{'email':user.username,'jobs':jobs,'message':message})  
        except Exception, e:
            pass
    return message_home(request) 

def _login(request,message=None):
    user = request.user
    is_freelancer,rol  = isFreelancer(user)
    if is_freelancer!=None:
        if user.is_authenticated():
            return redirect("/dashboard/")
    return render(request,'login.htm',{"message":message})

def _logout(request):
    logout(request)
    return redirect('/login/')

@require_GET
def check_user(request, email):
    email = email
    try:
        User.objects.get(email=email)            
        return HttpResponse("1")               
    except User.DoesNotExist: 
        return HttpResponse("0")   
    return message_home(request)

@require_GET
def activation(request, email, key):
    email   = email
    key     = key
    
    try:
        u = User.objects.get(email=email) 
        if key==md5.md5(u.email+u.last_name).hexdigest():
            u.is_active = True
            u.save(force_update=True)
            return render(request,'login.htm',{ 'message':'Su cuenta fue activada exitosamente.'})
        else:
            return message_home(request, "La clave no coincide, favor de ponerse en contacto con el equipo de soporte.")   
    except Exception,e:
        logger.error(e)
    return message_home(request, "El usuario no existe, favor de ponerse en contacto con el equipo de soporte.")  
    

@require_GET
def activation_signup(request, email, key, code):
    email   = email
    key     = key
    
    try:
        u = User.objects.get(email=email) 
        if key==md5.md5(u.email+u.last_name).hexdigest():
            u.is_active = True
            u.save(force_update=True)
            j = Job.objects.filter(code=code).update(state='1')
            if j:
                return render(request,'login.htm',{ 'message':'Su cuenta fue activada exitosamente y su proyecto fue publicado.'})
            else:
                return render(request,'login.htm',{ 'message':'Su cuenta fue activada exitosamente, recuerde activar su proyecto.'})
        else:
            return message_home(request, "La clave no coincide, favor de ponerse en contacto con el equipo de soporte.")   
    except Exception,e:
        logger.error(e)
        print e
    return message_home(request, "El usuario no existe, favor de ponerse en contacto con el equipo de soporte.")  
    

    
def isFreelancer(user):
    try:
        profile  = Freelancer.objects.get(user=user.pk) 
        return True, profile
    except Exception, e:
        pass
    try:
        profile = Employer.objects.get(user=user.pk)
        return False, profile
    except Exception, e:
        pass
    return None, None
