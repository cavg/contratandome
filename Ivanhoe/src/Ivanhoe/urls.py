# -*- coding: utf8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from Ivanhoe.settings import ROOT_DIR
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',                                          direct_to_template, {'template': 'index.htm'}),      
        
    url(r'^signup_freelancer/',                         direct_to_template, {'template': 'signup_freelancer.htm'}),
    url(r'^signup_freelancer_post/',                    'Ivanhoe.freelancer.views.signup_freelancer_post'),   
    url(r'^update_freelancer_account_post/',            'Ivanhoe.freelancer.views.update_account_freelancer_post'),
    url(r'^list_freelancers/',                          'Ivanhoe.freelancer.views.list_freelancers'),
       
    url(r'^signup_employer/(?P<type>.*)',               'Ivanhoe.employer.views.signup_employer'),
    url(r'^update_employer_account_post/',              'Ivanhoe.employer.views.update_account_employer_post'),     
    
        
    url(r'^add_service/',                               'Ivanhoe.job.views.add_service'),
    url(r'^add_service_post/',                          'Ivanhoe.job.views.add_service_post'), 
    url(r'^add_job/',                                   'Ivanhoe.job.views.add_job'),
    url(r'^jobs/',                                      'Ivanhoe.job.views.jobs'),
    url(r'^services/',                                  'Ivanhoe.job.views.services'),
    url(r'^jobs_freelancer/',                           'Ivanhoe.job.views.jobs_offered_to_freelancers'),  
    url(r'^jobs_freelancer_filtered_post/',              'Ivanhoe.job.views.jobs_offered_to_freelancers_filtered'),  
    url(r'^services_employer/',                         'Ivanhoe.job.views.services_offered_to_employers'),          
    url(r'^list_my_jobs/',                              'Ivanhoe.job.views.list_my_jobs'),
    url(r'^job/(?P<code>.*)',                           'Ivanhoe.job.views.view_job'),
    url(r'^job_contact/(?P<code>.*)',                   'Ivanhoe.job.views.view_job_contact'),
    url(r'^job_finish/(?P<code>.*)',                    'Ivanhoe.job.views.finish_job'),
    url(r'^delete_job/(?P<code>.*)/(?P<rol>.*)',        'Ivanhoe.job.views.delete_job'),   
    url(r'^invite_freelancers/(?P<code>.*)',            'Ivanhoe.job.views.invite_freelancers'),   
    url(r'^send_invitation/(?P<email>.*)/(?P<code>.*)', 'Ivanhoe.job.views.send_invitation'),   
    url(r'^anular_job/(?P<code>.*)',                    'Ivanhoe.job.views.anular_job'),
    
     
    url(r'^post_feedback/',                             'Ivanhoe.feedback.views.post_feedback'),  
    
    url(r'^write_comment_for_job/',                     'Ivanhoe.comment.views.write_comment_for_job'), 
    url(r'^reply_comment_for_job/',                     'Ivanhoe.comment.views.reply_comment_for_job'),     
    url(r'^postulate_to_job/',                          'Ivanhoe.postulate.views.postulate_to_job'),
    url(r'^freelancer_list_postulations/',              'Ivanhoe.postulate.views.freelancer_list_postulations'),
    url(r'^set_postulation/',                           'Ivanhoe.postulate.views.set_postulation'),    
     
    url(r'^freelancer_list_msgs/',                     'Ivanhoe.comment.views.freelancer_list_msgs'), 
    
    #pendiente ajuste para msg privados...
    url(r'^employer_list_msgs/',                       'Ivanhoe.comment.views.employer_list_msgs'),       
             
    url(r'^about/',                                     direct_to_template, {'template': 'about.htm'}),     
    url(r'^howpublish/',                                direct_to_template, {'template': 'howpublish.htm'}), 
    url(r'^howpostulate/',                              direct_to_template, {'template': 'howpostulate.htm'}),
    url(r'^profile/(?P<email>.*)',                     'Ivanhoe.shared.views.profile'),              
    url(r'^update_account/',                            'Ivanhoe.shared.views.update_account'),      
    url(r'^change_password/',                           'Ivanhoe.shared.views.change_password'),   
    url(r'^login/',                                     'Ivanhoe.shared.views._login'),
    url(r'^check_login/',                               'Ivanhoe.shared.views.check_login'),
    url(r'^dashboard/',                                 'Ivanhoe.shared.views.dashboard'),
    url(r'^logout/',                                    'Ivanhoe.shared.views._logout'),
    url(r'^activation/(?P<email>.*)/(?P<key>.*)',       'Ivanhoe.shared.views.activation'),    
    url(r'^activation-signup/(?P<email>.*)/(?P<key>.*)/(?P<code>.*)','Ivanhoe.shared.views.activation_signup'), 
    url(r'^check_user/(?P<email>.*)',                   'Ivanhoe.shared.views.check_user'),    
    url(r'^set_category_freelancer/(?P<category>.*)/(?P<state>.*)','Ivanhoe.user_classification.views.set_category_freelancer'),
    
    
    url(r'^set_category_job/(?P<category>.*)/(?P<state>.*)/(?P<job_id>.*)','Ivanhoe.job_classification.views.set_category_job'),    
        
    url(r'^categories/(?P<id>.*)',                      'Ivanhoe.classification.views.get_categories'),     
        
    url(r'^define_evaluation/(?P<code>.*)',             'Ivanhoe.aspect.views.define_evaluation'),
    url(r'^set_aspect/(?P<code>.*)/(?P<id>.*)/(?P<state>.*)/(?P<user>.*)','Ivanhoe.aspect.views.set_aspect'),  
    
    url(r'^evaluate/(?P<code>.*)/(?P<user>.*)'           ,'Ivanhoe.rate.views.evaluate'), 
    url(r'^evaluate_post/'                              ,'Ivanhoe.rate.views.evaluate_post'),       
    
    
    #url(r'^rate_evaluation/(?P<code>.*)',             'Ivanhoe.aspect.views.rate_evaluation'),
       
    url(r'^admin/doc/',                                 include('django.contrib.admindocs.urls')),
    url(r'^admin/',                                     include(admin.site.urls)),    
    (r'^(?P<path>.*)$',                                 'django.views.static.serve', {'document_root': ROOT_DIR}),
        

)
