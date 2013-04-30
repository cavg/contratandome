from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from Ivanhoe.comment.models import Comment, ViewComment
from Ivanhoe.job.models import Job
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from Ivanhoe.settings import URL
from Ivanhoe.Util.Email import Email


@require_POST
@login_required
def write_comment_for_job(request):
    try:
        author      = request.POST["author"]
        job         = request.POST["job"]
        text        = request.POST["text"]
        to          = request.POST["to"]
                
        co = Comment(author=User.objects.get(id=author),job=Job.objects.get(id=job),text=text,to_user=to)
        co.save()
        
        try:
            user = User.objects.get(id=to)
            email = user.email
            send_email(email)  
        except Exception,e:
            print e
        
        return redirect("/jobs_freelancer/")
    except Exception,e:
        print e
    return redirect("/jobs_freelancer/")

def send_email(recipient):
    login_url = URL+"/login/"
        
    msg_text = u"""
        Estimado usuario, <br><br>
        Ha recibido un mensaje. Para revisarlo por favor ingrese a su cuenta.<br><br>
        <a href=\"%s\" target='_blank'>%s</a>            
        <br><br>
        Atte.<br>
        Equipo de desarrollo.<br>contratando ME """ % (login_url, login_url)  
        
    EmailSend = Email() 
    EmailSend.send(recipients=[recipient], subject='Tiene un nuevo mensaje en ContratandoME', message_plaintext=msg_text, message_html=msg_text, default_from_mail='Contratandome <no-reply@contratando.me>')
 
@require_POST
@login_required
def reply_comment_for_job(request):
    try:
        author              = request.POST["author"]
        job                 = request.POST["job"]
        text                = request.POST["text"]
        to                  = request.POST["to"]
        referenced_comment  = request.POST["referenced_comment"]
        
        
        job=Job.objects.get(id=job)
        co = Comment(author=User.objects.get(id=author),job=job,text=text,to_user=to,referenced_comment=referenced_comment)
        co.save()
        
        try:
            user = User.objects.get(id=to)
            email = user.email
            send_email(email)  
        except Exception,e:
            print e
        
        return redirect("/job/"+job.code)
    except Exception,e:
        print e
    return redirect("/job/"+job.code)

@login_required
def employer_list_msgs(request): 
    msgs = []
    f_msgs  = Comment.objects.filter(to_user=request.user.id, type='DM')
    for msg in f_msgs:
        f_job = "%s" % msg.job.short_description
        vc    = ViewComment(f_id=msg.id,f_author=msg.author.id,f_datetime=msg.datetime,f_to_user=msg.to_user,f_job=f_job,f_text=msg.text,f_subject=msg.subject,f_is_viewed=msg.is_viewed,job_id=msg.job.id)       
        try:
            r_msg = Comment.objects.get(referenced_comment=msg.id)
            vc.set_response(r_id=r_msg.id, r_author=r_msg.author, r_to_user=r_msg.to_user , r_job=r_msg.job, r_text=r_msg.text, r_subject=r_msg.subject, r_datetime=r_msg.datetime, r_is_viewed=r_msg.is_viewed)
        except Exception,e:
            print e        
        msgs.append(vc)    
    
    return render(request,"employer_msgs.htm",{'msgs':msgs})    
    
    
@login_required
def freelancer_list_msgs(request): 
    msgs = []
    print request.user.first_name,request.user.id
    f_msgs  = Comment.objects.filter(author=request.user, type='DM')
    for msg in f_msgs:
        f_job = "%s" % msg.job.short_description
        vc    = ViewComment(f_id=msg.id,f_author=msg.author.id,f_datetime=msg.datetime,f_to_user=msg.to_user,f_job=f_job,f_text=msg.text,f_subject=msg.subject,f_is_viewed=msg.is_viewed,job_id=msg.job.id)       
        try:
            r_msg = Comment.objects.get(referenced_comment=msg.id)
            vc.set_response(r_id=r_msg.id, r_author=r_msg.author, r_to_user=r_msg.to_user , r_job=r_msg.job, r_text=r_msg.text, r_subject=r_msg.subject, r_datetime=r_msg.datetime, r_is_viewed=r_msg.is_viewed)
        except Exception,e:
            print e            
        msgs.append(vc)    
    
    return render(request,"freelancer_msgs.htm",{'msgs':msgs})
    
