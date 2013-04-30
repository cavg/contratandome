#!/usr/bin/python
# -*- coding: utf8 -*-

from django.db import models
from Ivanhoe.classification.models import Classification, META_CATEGORIES

TYPE    = (('General', 'General'),('Especifico', 'Específico'),)
USER    = (('Empresa','Empresa'),('Freelancer','Freelancer'),('Ambos','Ambos'))

#http://www.quintcareers.com/job_skills_values.html
#http://www.kent.ac.uk/careers/sk/skillsinjobs.htm
#http://www.kent.ac.uk/careers/compet/skillquest.htm
#http://career.cabalgroup.com/exercises/professional_skillls.htm
#https://docs.google.com/viewer?a=v&q=cache:nfYsBbWpTcsJ:www.tasc.sa.gov.au/LinkClick.aspx%3Ffileticket%3DAJRaOy5z4UE%253D%26tabid%3D126+&hl=es&gl=cl&pid=bl&srcid=ADGEESjFf-jQKJCR4na0FtyDxUCmW0Gfkt8YQ2zxUg736Jh9L9P_5e6giICaIL9QxqV_IBRppE9jJxw9Noz0nwDhg4cj5h9Y5CL9fab69xwi2TOhhjZgwRhkr9FyqdBHTxsmCc9ghVKx&sig=AHIEtbRNNULlxPH3QJ99Gh_E4dpTSgvNaA
#http://jobs.aol.com/articles/2009/01/26/top-10-soft-skills-for-job-hunters/
#http://jobsearchtech.about.com/od/computerjob13/a/compjobskills_2.htm
#http://designreviver.com/articles/10-essential-skills-every-graphic-designer-should-have/
#http://www.slideshare.net/almagreta/top-10-graphic-designer-skills
#http://www.fastcompany.com/blog/ken-musgrave/thinkdesign/beyond-design-10-skills-designers-need-succeed-now
#http://www.mindtools.com/pages/article/sales-skills.htm
#http://www.smartcompany.com.au/people-problems/eve-ash-24568.html
#http://www.ehow.com/list_6645174_skills-needed-receptionist-jobs_.html
#http://www.hoadley.net/barbara/courses/receptionist.htm


class Aspect(models.Model):
    classification  = models.CharField(max_length=30,choices=META_CATEGORIES,null=True,blank=True)
    name            = models.TextField(max_length=20)
    description     = models.TextField()
    type            = models.CharField(max_length=20, choices=TYPE)
    user            = models.CharField(max_length=20, choices=USER)
    extended_eval   = models.BooleanField()
    
    
    def __unicode__(self):
        return "%s - %s - %s" % (self.name,self.type, self.user)