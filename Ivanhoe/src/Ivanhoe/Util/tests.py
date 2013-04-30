#!/usr/bin/python
# -*- coding: utf8 -*-
from django.conf import settings
from Ivanhoe.Util.Email import Email
from django.test import TestCase

class Test(TestCase):
    def test_send(self):
    	EmailSend = Email()
    	EmailSend.send()
    	self.assertEquals(len(EmailSend.outbox), 1)
    	print EmailSend.outbox