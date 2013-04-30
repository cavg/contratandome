from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Ivanhoe.feedback.models import Feedback
from django.http import HttpResponse
from Ivanhoe.Util.Util import message_employer, message_freelancer
from Ivanhoe.shared.views import isFreelancer, dashboard


@login_required
def post_feedback(request):
    
    is_freelancer, rol = isFreelancer(request.user)
    
    try:
        email   = request.POST["email"]
        comment = request.POST["comment"]
        rol     = request.POST["rol"]
        
        fb = Feedback(comment=comment, user=email)
        fb.save()
        
        if is_freelancer==False:
            return dashboard(request,message="Su comentario fue enviado.")
        elif is_freelancer==True:
            return dashboard(request,message="Su comentario fue enviado.")       
    except Exception,e:
        print e
    return redirect("/dashboard/")
    