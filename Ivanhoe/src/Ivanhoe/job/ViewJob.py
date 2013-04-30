#!/usr/bin/python
# -*- coding: utf8 -*-
from django.contrib.auth.models import User
from Ivanhoe.job_classification.models import Job_classification
from Ivanhoe.classification.models import Classification
from Ivanhoe.postulate.models import Postulate, ViewPostulate
from Ivanhoe.comment.models import Comment, ViewComment
from Ivanhoe.rate.models import RateView, Rate
from Ivanhoe.Util.Util import isFreelancer
from datetime import datetime,timedelta

class ViewJob():
    
    def __init__(self,id='',offer_id='',offer_name='',offer_email='',short_description='',extended_description='',budget=0,publication='',code='',type='',classification=[],postulations=list(),comments=list(),assigned=None, rates_employer=None,rates_freelancer=None, state=''):
        self.id                      = id
        self.offer_id                = offer_id
        self.offer_name              = offer_name
        self.offer_email             = offer_email
        self.state                   = state
        
        self.short_description       = short_description
        self.extended_description    = extended_description
        self.budget                  = budget
        self.publication             = publication
        self.code                    = code
        self.type                    = type
        
        self.classification          = classification  
        self.postulations            = postulations
        self.comments                = comments
        self.assigned                = assigned
        self.rates_employer          = rates_employer #para evaluar a employer
        self.rates_freelancer        = rates_employer #para evaluar a freelancers
        self.score_employer          = 0.0
        self.score_freelancer        = 0.0
        self.rate_out_of_date_f      = None 
        self.rate_out_of_date_e      = None
        self.finish                  = None
        self.experience_days         = 1
        self.state                   = state
        
                
    def to_full_jobView(self,j):
        try:
            user                        = User.objects.get(username=j.offer)
            offer_name                  = "%s %s" % (user.first_name, user.last_name)
            self.offer_name             = offer_name
            self.offer_email            = user.email
            self.offer_id               = user.id
            self.id                     = j.id
            self.short_description      = j.short_description
            self.extended_description   = j.extended_description
            self.budget                 = j.budget
            self.publication            = j.publication
            self.code                   = j.code
            self.type                   = j._type
            self.state                  = j.state
            self.assigned               = j.assigned
            self.fixed_price            = j.fixed_price
            self.finish                 = "%s" % str(j.finish).split(" ")[0]            
        except Exception, e:
            pass     
        try:
            job_c   = Job_classification.objects.filter(job=j)
            self.classification = []
            for jc in job_c:
                try:
                    cl = Classification.objects.get(id=jc.classification.pk)
                    self.classification.append(cl.name)
                except Exception,e:
                    pass         
        except Exception, e:
            pass
        
        try:
            self.postulations = list()
            ps  = Postulate.objects.filter(job=j).order_by('-is_accepted')
            for p in ps:
                #si hay una postulación aceptada solo se carga esa, de lo contrario se cargan todas (rechazadas y no revisadas)
                if p.is_accepted=='1': 
                    vp = ViewPostulate(id=p.id,date=p.date,detail=p.detail,is_accepted=p.is_accepted,job=p.job.id,job_name=p.job.short_description, price=p.price,user=p.user,cause= p.cause, timestamp= p.timestamp)
                    self.postulations.append(vp)
                    break
                else:
                    vp = ViewPostulate(id=p.id,date=p.date,detail=p.detail,is_accepted=p.is_accepted,job=p.job.id,job_name=p.job.short_description, price=p.price,user=p.user,cause= p.cause, timestamp= p.timestamp)
                    self.postulations.append(vp)    
            try:
                f_msgs  = Comment.objects.filter(job=j,referenced_comment=None, type='DM')
                self.comments = list()
                for msg in f_msgs:
                    f_job = "%s" % msg.job.short_description
                    vc    = ViewComment(f_id=msg.id,f_author=msg.author,f_datetime=msg.datetime,f_to_user=msg.to_user,f_job=f_job,f_text=msg.text,f_subject=msg.subject,f_is_viewed=msg.is_viewed,job_id=msg.job.id)       
                    try:
                        r_msg = Comment.objects.get(referenced_comment=msg.id)
                        vc.set_response(r_id=r_msg.id, r_author=r_msg.author, r_to_user=r_msg.to_user , r_job=r_msg.job, r_text=r_msg.text, r_subject=r_msg.subject, r_datetime=r_msg.datetime, r_is_viewed=r_msg.is_viewed)
                    except Exception,e:
                        pass      
                    self.comments.append(vc) 
            except Exception,e:
                pass 
        except Exception,e:
            pass
        
        # getting aspect to evaluate  
          
        rate_date_employer   = None         
        try:
            rates               = Rate.objects.filter(job=j, user=j.offer)
            if len(rates)>0:
                self.rates_employer   = []
                valid_rates = 0.0
                for r in rates:
                    if r.score!=0:
                        #print "(employer) score: %s  job name: %s" % (r.score, self.name)
                        rate_date_employer = r.evaluation_date
                        
                        valid_rates = valid_rates+1.0
                        self.score_employer += r.score
                        
                    rv = RateView(aspect=r.aspect,job=r.job,score=r.score,creation_date=r.creation_date,evaluation_date = r.evaluation_date)
                    self.rates_employer.append(rv) 
                self.score_employer = round((self.score_employer/(valid_rates*3))*10, 1)                
        except Exception,e:
            pass
        
        
        if rate_date_employer!=None:
            self.is_employer_out_of_date(rate_date_employer)
        
        
        
        rate_date_freelancer   = None 
        try:
            rates               = Rate.objects.filter(job=j, user=j.assigned.user)
            if len(rates)>0:
                self.rates_freelancer   = []
                valid_rates = 0.0
                for r in rates:
                    #print r.evaluation_date
                    if r.score!=0:
                        #print "(freelancer) score: %s  job name: %s" % (r.score, self.name)
                        rate_date_freelancer = r.evaluation_date
                        
                        valid_rates = valid_rates+1.0
                        self.score_freelancer += r.score
                        
                    rv  = RateView(aspect=r.aspect,job=r.job,score=r.score,creation_date=r.creation_date,evaluation_date = r.evaluation_date)
                    self.rates_freelancer.append(rv) 
                self.score_freelancer = round((self.score_freelancer/(valid_rates*3))*10,1)
        except Exception,e:
            pass          
        
        if rate_date_freelancer!=None:
            self.is_freelancer_out_of_date(rate_date_freelancer)
       
        
        self.calculate_experience()
        
        
    def is_freelancer_out_of_date(self,rate_date_freelancer):
        try:
            finish_date = str(self.finish).split("-")
            proj_date = datetime(int(finish_date[0]),int(finish_date[1]),int(finish_date[2]))
            
            proj_date_plus_month  = proj_date+timedelta(days=+30)
            
            rate_date_e = str(rate_date_freelancer).split("-")
            p_r_f = datetime(int(rate_date_e[0]),int(rate_date_e[1]),int(rate_date_e[2]))
            
            if p_r_f>proj_date_plus_month:
                self.rate_out_of_date_f = True
            else:
                self.rate_out_of_date_f = False
        except Exception,e:
            print e

    def calculate_experience(self):
        a_end = str(self.finish).split("-")
        s_ini = str(self.publication).split(" ")[0]
        a_ini = s_ini.split("-")
        date_ini = datetime(int(a_ini[0]),int(a_ini[1]),int(a_ini[2]))
        date_end = datetime(int(a_end[0]),int(a_end[1]),int(a_end[2]))
        self.experience_days = (date_end-date_ini).days
        if self.experience_days == 0:
            self.experience_days = 1
    
    def is_employer_out_of_date(self,rate_date_employer):
        try:
            finish_date = str(self.finish).split("-")
            proj_date = datetime(int(finish_date[0]),int(finish_date[1]),int(finish_date[2]))
            
            proj_date_plus_month  = proj_date+timedelta(days=+30)
            
            rate_date_e = str(rate_date_employer).split("-")
            p_r_e = datetime(int(rate_date_e[0]),int(rate_date_e[1]),int(rate_date_e[2]))
            
            if p_r_e>proj_date_plus_month:
                self.rate_out_of_date_e = True
            else:
                self.rate_out_of_date_e = False
        except Exception,e:
            print e
        
        
    def is_rated(self, user):
        is_freelancer,user_rol = isFreelancer(user) 
        try:   
            if is_freelancer==True:  
                for r in self.rates_freelancer:
                    if r.score==0:
                        return 0
                    else:
                        return 1
            elif is_freelancer==False:
                for r in self.rates_employer:
                    if r.score==0:
                        return 0
                    else:
                        return 1
        except Exception,e:
            pass
        return None
        
        
    