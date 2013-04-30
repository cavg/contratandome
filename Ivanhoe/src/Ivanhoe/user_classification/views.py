from django.views.decorators.http import require_GET
from django.contrib.auth.models import User
from Ivanhoe.classification.models import Classification
from Ivanhoe.user_classification.models import User_classification
from django.http import HttpResponse


@require_GET
def set_category_freelancer(request,category,state):   
     
    u = User.objects.get(username=unicode(request.user)) 
    c = Classification.objects.get(name=category)        
   
    try:
        uc = User_classification.objects.get(classification=c, user=u)
        if state!="True": 
            uc.delete()
    except Exception, e:
        pass
        #logger.error(e)
        if state!="True":
            uc = User_classification(classification=c, user=u)
            uc.save()    
    try:
        r = category+''+state+unicode(request.user)
    except Exception,e:
        pass
        #logger.error(e)
    return HttpResponse('<p>'+r+'</p>');
