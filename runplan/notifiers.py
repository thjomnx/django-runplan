from __future__ import unicode_literals

from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse

from runplan.models import Settings
from runplan.settings import *
from runplan.utils import *

class Notification():
    def __init__(self, request, run, code):
        self.request = request
        self.run = run
        self.code = code
    
    def send(self):
        finalize_account(self.request.user)
        
        accounts = []
        
        for o in self.run.observation_set.all():
            if o.author not in accounts:
                accounts.append(o.author)
        
        if self.code == 'run.create':
            for s in Settings.objects.filter(emailon_newrun=True):
                if s.account not in accounts:
                    accounts.append(s.account)
        
        if self.code == 'run.edit':
            for s in Settings.objects.filter(emailon_modifiedrun=True):
                if s.account not in accounts:
                    accounts.append(s.account)
        
        if self.code == 'run.cancel':
            for s in Settings.objects.filter(emailon_canceledrun=True):
                if s.account not in accounts:
                    accounts.append(s.account)
        
        for s in Settings.objects.filter(emailon_activity=True):
            if s.account not in accounts:
                accounts.append(s.account)
        
        bcc_list = []
        
        for a in accounts:
            bcc_list.append(a.email)
        
        subject = email_subject_prefix + email_subject_templates[self.code]
        subject = subject % {'user': self.request.user.get_full_name(), 'run': self.run.track_name}
        
        if email_body_header:
            message = email_body_header + '\n\n'
        else:
            message = ''
        
        message += email_body_templates[self.code]
        message = message % {'link': self.request.build_absolute_uri(reverse('runplan.views.detail', args=(self.run.id,)))}
        
        if email_body_footer:
            message += '\n\n' + email_body_footer
        
        email = EmailMessage(subject, message, email_from_addr, bcc=bcc_list)
        email.send()
