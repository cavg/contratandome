#!/usr/bin/python
# -*- coding: utf8 -*-
from django.conf import settings
from asynchronous_send_mail import send_mail
from Ivanhoe.settings import LOGGER
import logging
logger = logging.getLogger(LOGGER)


class Email():
	def send(self, recipients=['camilo.verdugo@gmail.com'], subject='test', message_plaintext='test', message_html='<b>test</b><h1>lalal</h1>', default_from_mail='Contratandome <no-reply@contratando.me>'):
		try:
			send_mail(subject, message_plaintext, default_from_mail, recipients, False, message_html)
			logger = logging.getLogger('info.log')
			logger.info("to %s, subject %s , text %s"%(recipients[0],subject,message_plaintext))
		except Exception, e:
			logger = logging.getLogger('error.log')
			logger.error("sending mail to %s" % recipients[0])
		
