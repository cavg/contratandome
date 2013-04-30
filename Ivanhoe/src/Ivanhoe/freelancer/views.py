# -*- coding: utf8 -*-
from django.contrib.auth.models import User
from Ivanhoe.freelancer.models import Freelancer, UserProfile
from django.views.decorators.http import require_POST
from Ivanhoe.settings import SITE_NAME, URL
import md5
from django.contrib.auth.decorators import login_required
from django_countries.countries import COUNTRIES
from Ivanhoe.user_classification.models import User_classification
from Ivanhoe.classification.models import Classification
from Ivanhoe.Util.Email import Email
from django.shortcuts import render
from Ivanhoe.job.models import Job
from Ivanhoe.job_classification.models import Job_classification
from django.http import HttpResponse
from Ivanhoe.Util.Util import message_home, message_freelancer
import datetime

#TODO:[x] Add access to all services available.
#TODO: Dashboard with process diagram for friendly interface
#TODO: New feature: Interview indicating datetime available.


#TODO: [18 mayo] Freelancer's Profile: Skills, bio, contact info, evaluation reports, grades.
@require_POST
def signup_freelancer_post(request):
    try:
        first_name  = request.POST["first_name"]
        last_name   = request.POST["last_name"]
        email       = request.POST["email"]
        password    = request.POST["password"]  
        
        u = User(first_name=first_name, last_name=last_name, email=email, username=email, is_active=False)
        u.set_password(password)
        u.save(force_insert=True, force_update=False)
       
        f = Freelancer(user_id=u.pk, phone="")
        f.save()
        
                
        url_activation  = URL+'/activation/%s/%s' % (email, md5.md5(email+last_name).hexdigest())
        
        msg_text = u"""
        Bienvenido a %s <br><br>
        Gracias por registrarse en nuestro sitio, ahora ya podr&aacutes disfrutar de nuestros servicios completamente gratis!!!<br>
        Para activar su cuenta, solo debes hacer click sobre el siguiente enlace.<br><br>
        <a href=\"%s\" target='_blank'>%s</a>
        <br><br>
        Atte.<br>
        Equipo de desarrollo.<br>contratando ME """ % (SITE_NAME, url_activation, url_activation)  
        
        EmailSend = Email()        
        EmailSend.send(recipients=[email], subject='Bienvenido a ContratandoME', message_plaintext=msg_text, message_html=msg_text, default_from_mail='Contratandome <no-reply@contratando.me>')
        return render(request,'login.htm',{"message":"El registro fue exitoso. Revise su casilla de correo para activar su cuenta."})
    except Exception, e:
        #logger.error(e)
        pass
    return message_home(request)
        
        

#TODO:[x] Selected Chile as country and preload cities.
@login_required
def update_account_freelancer(request,message=None):
    try:
        user = request.user 
        user_classifications = []    
   
        uc = User_classification.objects.filter(user=user)
        for u in uc:
            c = Classification.objects.get(id=u.classification_id)
            user_classifications.append(c.name)
                
        freelancer  = Freelancer.objects.get(user=user.pk)     
        if freelancer.phone == None:
            freelancer.phone = ''
        if freelancer.hh_cost == 0.000:
            freelancer.hh_cost = ''
           
        return render(request, 'update_freelancer_account.htm', {'countries':COUNTRIES, 'user':user,'freelancer':freelancer,'selected':user_classifications,'message':message})
    except Exception,e:
        #logger.error(e)
        pass
    return message_freelancer(request)

@login_required
def update_account_freelancer_post(request):
    try:    
        #profession      = request.POST["profession"]
        user_id         = request.POST["user_id"]
        web_site        = request.POST["web_site"]
        address         = request.POST["address"]
        phone           = request.POST["phone"]   
        country         = request.POST["country"]
        hh_cost         = request.POST["hh_cost"].replace(',','.')
        hh_cost         = hh_cost.replace('$','')
        city            = request.POST["city"]     
        bio             = request.POST["bio"]  
        
        if hh_cost == '':
            hh_cost = '0.000'
        
        Freelancer.objects.filter(user=user_id).update(web_site=web_site, address=address,phone=phone,country=country,hh_cost=hh_cost, city=city, bio=bio)             
        
        now = datetime.datetime.now()
        update_hour = "(%s:%s:%s)" % (now.hour, now.minute, now.second)
        return update_account_freelancer(request, message="Sus datos fueron actualizados %s"%update_hour)
    except Exception,e:
        return update_account_freelancer(request)
        pass
    return message_freelancer(request)
    
    
    
def list_freelancers(request):
    freelancers = get_freelancers(limit=None)
    return render(request,'list_freelancers.htm',{'freelancers':freelancers})

def get_freelancers(limit=5):
    users = []
    if limit==None:
        users = User.objects.filter(is_active=1, is_staff=0).order_by('last_login')
    else:
        users = User.objects.filter(is_active=1, is_staff=0).order_by('last_login')[:limit]
    freelancers = []
    for u in users: 
        try:            
            free = UserProfile()
            free.categories = []
            try:
                ucs = User_classification.objects.filter(user=u)
                for uc in ucs:
                    try:
                        c = Classification.objects.get(id=uc.classification_id)
                        free.categories.append(c.name)
                    except Exception,e:
                        pass
            except Exception,e:
                pass          
            try:
                f = Freelancer.objects.get(user=u)  
                free.web_site   = f.web_site
                free.address    = f.address
                free.country    = f.country
                free.city       = f.city
                free.phone      = f.phone
                free.bio        = f.bio
                free.first_name = u.first_name
                free.last_name  = u.last_name
                free.email      = u.email
                freelancers.append(free)
            except Exception,e:
                pass                
        except Exception,e:
            pass
    return freelancers   



