# -*- coding: utf8 -*-
from django.shortcuts import *
from django.contrib.auth.models import User
from Ivanhoe.employer.models import Employer
from Ivanhoe.settings import CONTACT_EMAIL, SITE_NAME, URL, LOGIN_URL#, logger
from django.core import mail
import md5, sys
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from Ivanhoe.user_classification.models import User_classification
from Ivanhoe.classification.models import Classification, META_CATEGORIES
from django_countries.countries import COUNTRIES
from Ivanhoe.job_classification.models import Job_classification
from Ivanhoe.Util.Email import Email
from Ivanhoe.job.models import Job
import random
import re
from Ivanhoe.Util.Util import message_employer, message_home
import datetime
import logging
from Ivanhoe.settings import LOGGER

logger = logging.getLogger(LOGGER)

def signup_employer(request, type="default"): 
    try:    
        if request.method=='POST':     
            categories      = request.POST["categories"]
            names           = request.POST["name"]
            lnames          = len(names.split(" "))
            if lnames==2:
                first_name  = names.split(" ")[0]
                last_name   = names.split(" ")[1]
            elif lnames==1:
                first_name  = names.split(" ")[0]
                last_name   = ''
            else:
                first_name  = ''
                last_name   = ''
            name_company    = ''
            email           = request.POST["email"]
            country         = ''
            phone1          = ''
            city            = ''
            name_job        = request.POST["short_description"]
            description     = request.POST["extended_description"]
            budget          = request.POST["budget"]
            if budget != '':
                budget = int(re.sub("\D","",budget))
            else:
                budget = 0
            password        = password_generator().strip()     
            fixed_price     = request.POST["is_fixed"] 
            is_public       = request.POST["is_public"]
                    
            is_new_user,_id     = signup_job_post(_id=None,first_name=first_name,last_name=last_name,name_company=name_company,email=email,
                                              country=country,phone1=phone1,city=city,name_job=name_job,description=description,
                                              budget=budget, code='',password=password, fixed_price=fixed_price, is_public=is_public)
            code = md5.md5(str(_id)).hexdigest()
            Job.objects.filter(id=_id).update(code=code)

            url_activation  = URL+'/activation-signup/%s/%s/%s' % (email,str(md5.md5(email+last_name).hexdigest()),code)
            
            url_job         = URL+'/job/'+str(code)
            url_login       = URL+'/login/'

            EmailSend =  Email()

            categories_a = categories.split(",")
            for i in categories_a:
                if len(i)>1:
                    c = Classification.objects.get(name=i)   
                    jc = Job_classification(classification=c, job=Job.objects.get(id=_id))        
                    jc.save()         

            if is_new_user:
                msg_text = u"""
                Bienvenido a %s <br><br>
                Gracias por registrarse en nuestro sitio, ahora ya podras disfrutar de nuestros servicios completamente gratis!!!<br>
                Para activar su cuenta, solo debes hacer click sobre el siguiente enlace.<br><br>
                <a href=\"%s\" target='_blank'>%s</a>
                <br><br>
                Su publicación se encuentra disponible en:<br><br>
                <a href=\"%s\" target='_blank'>%s</a>
                <br><br>
                Su contraseña es:<br>
                <b>%s</b>
                <br><br>
                Atte.<br>
                Equipo de desarrollo.<br>contratando ME """ % (SITE_NAME, url_activation, url_activation, url_job, url_job, password)  
                EmailSend.send(recipients=[email], subject='Bienvenido a ContratandoME', message_plaintext=msg_text, message_html=msg_text, default_from_mail='Contratandome <no-reply@contratando.me>')
            else:
                msg_text = u"""
                Su oferta fue publicada exitosamente y se encuentra disponible en:<br><br>        
                <a href=\"%s\" target='_blank'>%s</a>
                <br><br>
                Recuerde actualizar su perfil en:<br>
                <a href=\"%s\" target='_blank'>%s</a>
                <br><br>
                Atte.<br>
                Equipo de desarrollo.<br>contratando ME """ % (url_job, url_job, url_login,url_login)
                EmailSend.send(recipients=[email], subject='ContratandoME su oferta de trabajo fue publicada', message_plaintext=msg_text, message_html=msg_text, default_from_mail='Contratandome <no-reply@contratando.me>')
            return render(request,'login.htm',{"message":"Su proyecto fue ingresado. Revise su casilla de correo para activar su cuenta."})
        else:
            types=(('ti','1','informáticos'),('design','2','diseñadores'),('scriptures','3','redactores'),('ads','4','expertos en marketing en linea'),('administration','5','expertos en administración'), ('consultancies','6','consultores'), ('legal','7','asesores legal'),('engineering','8','ingenieros'))   
            for k,v,v2 in types:
                if k==type:
                    return render(request,'signup_employer_category.htm',{'countries':COUNTRIES,"categories":META_CATEGORIES, 'job_category':v, 'profession':v2})
            return render(request,'signup_employer.htm',{'countries':COUNTRIES,"categories":META_CATEGORIES}) 
    except Exception, e:
        logger.error(e)

@login_required
def update_account_employer(request,message=None):
    try:
        user = User.objects.get(id=request.user.id)       
        user_classifications = []    
    
        uc = User_classification.objects.filter(user=user)
        for u in uc:
            c = Classification.objects.get(id=u.classification_id)
            user_classifications.append(c.name)
        employer  = Employer.objects.get(user=user.pk)
        
        return render(request, 'update_employer_account.htm', {'countries':COUNTRIES, 'user':user,'employer':employer,'message':message})
    except Exception,e:
        pass
        #logger.error(e)
    return message_employer(request) 
    



@login_required
def update_account_employer_post(request):
    try:    
        employer_id     = request.POST["employer_id"]
        user_id         = request.POST["user_id"]
        name            = request.POST["company"]
        address         = request.POST["address"]
        web_site        = request.POST["web_site"]
        phone1          = request.POST["phone1"]
        phone2          = request.POST["phone2"]        
        country         = request.POST["country"]        
        first_name      = request.POST["first_name"]
        last_name       = request.POST["last_name"]
        
        User.objects.filter(id=user_id).update(first_name=first_name,last_name=last_name)
        Employer.objects.filter(id=employer_id).update(name=name,address=address,web_site=web_site,phone1=phone1, phone2=phone2,country=country)
        
        now = datetime.datetime.now()
        update_hour = "(%s:%s:%s)" % (now.hour, now.minute, now.second)
        return update_account_employer(request, message="Sus datos fueron actualizados %s" % update_hour)
    except Exception,e:
        return redirect("/update_account/")
        pass
    return message_employer(request) 
    

def password_generator():
    return ''.join(random.choice("QWERTYUIOPASDFGHJKLZXCVBNM123456789") for x in range(6))


def signup_job_post(_id,first_name,last_name,name_company,email,country,phone1,city,name_job,description,budget,code,password,fixed_price, is_public): 
    is_new_user     = False
            
    try:
        user = User.objects.get(email=email)               
        User.objects.filter(email=email).update(first_name = first_name, last_name = last_name, username=email,is_active=1) 
    except Exception,e:
        user = User(first_name = first_name, last_name = last_name, email=email, username=email,is_active=0)           
        user.set_password(password)
        user.save()
        is_new_user = True            
    try:
        employer = Employer.objects.get(user=user) 
        Employer.objects.filter(user=user).update(name=name_company, phone1=phone1,country=country, city=city)
    except Exception,e:        
        employer = Employer(user=user, name=name_company, web_site='', address='', phone1=phone1, phone2='', country=country, city=city)
        employer.save()   
    try:
        if is_new_user==True:
            state = '-1'
        else:
            state = '1'
        if _id==None:
            job = Job(offer=user,short_description=name_job, extended_description=description,  budget=budget,fixed_price=fixed_price, public=is_public, state=state)
            job.save()
            _id = str(job.id)
            Job.objects.filter(id=_id).update(code=md5.md5(_id).hexdigest())
        else:
            Job.objects.filter(id=_id).update(offer=user,short_description=name_job, extended_description=description,  budget=budget, code=md5.md5(_id).hexdigest(),fixed_price=fixed_price, public=is_public, state=state)
    except Exception, e:
        print e
    return is_new_user,_id
