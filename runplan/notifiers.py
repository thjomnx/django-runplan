from __future__ import unicode_literals

from django.core.mail import EmailMessage

from runplan.models import Settings
from runplan.settings import *

class Notification():
    def __init__(self, run, activity):
        self.run = run
        self.activity = activity
    
    def send(self):
        accounts = []
        
        for o in self.run.observation_set.all():
            if o.author not in accounts:
                accounts.append(o.author)
        
        if self.activity.code == 'run.create':
            for s in Settings.objects.filter(emailon_newrun=True):
                if s.account not in accounts:
                    accounts.append(s.account)
        
        for s in Settings.objects.filter(emailon_activity=True):
            if s.account not in accounts:
                accounts.append(s.account)
        
        bcc_list = []
        
        for a in accounts:
            bcc_list.append(a.email)
        
        subject = email_subject_templates[self.activity.code]
        message = email_body_templates[self.activity.code]
        
        email = EmailMessage(subject, message, email_from_addr, bcc=bcc_list)
        email.send()
