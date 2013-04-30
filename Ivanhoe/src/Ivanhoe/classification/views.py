from Ivanhoe.classification.models import META_CATEGORIES, Classification
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from Ivanhoe.settings import LOGGER
import logging
logger = logging.getLogger(LOGGER)

@require_GET
def get_categories(request,id):
    r = []
    value = ''
    for k,v in META_CATEGORIES:
        if k==id:
            value = v
            break
      
    try:
        cats = Classification.objects.filter(category=value)         
        for c in cats:
            r.append(c.name)
    except Exception,e:
        logger.error("get categories %s" % e)
    return HttpResponse(','.join(r))