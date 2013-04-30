#!/usr/bin/python
# -*- coding: utf8 -*-
from Ivanhoe.freelancer.models import Freelancer
from Ivanhoe.employer.models import Employer
from django.shortcuts import render


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


def message_employer(request, message="Se produjo un error, nuestro equipo ya fue notificado.", img_file_name='info.png', href='/dashboard/'):
    return render(request,'message_employer.htm', {'message': message,'href':href,'img_file_name':img_file_name})

def message_freelancer(request, message="Se produjo un error, nuestro equipo ya fue notificado.", img_file_name='info.png', href='/dashboard/'):
    return render(request,'message_freelancer.htm', {'message': message,'href':href,'img_file_name':img_file_name})

def message_home(request, message="Se produjo un error, nuestro equipo ya fue notificado.", img_file_name='info.png', href='/'):
    return render(request,'message.htm', {'message': message,'href':href,'img_file_name':img_file_name})