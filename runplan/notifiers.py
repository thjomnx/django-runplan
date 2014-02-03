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
        
        subject = EMAIL_SUBJECT_PREFIX + EMAIL_SUBJECT_TEMPLATES[self.code]
        subject = subject % {'user': self.request.user.get_full_name(), 'run': self.run.track_name}
        
        if EMAIL_BODY_HEADER:
            message = EMAIL_BODY_HEADER + '\n\n'
        else:
            message = ''
        
        message += EMAIL_BODY_TEMPLATES[self.code]
        message = message % {'link': self.request.build_absolute_uri(reverse('runplan.views.detail', args=(self.run.id,)))}
        
        if EMAIL_BODY_FOOTER:
            message += '\n\n' + EMAIL_BODY_FOOTER
        
        email = EmailMessage(subject, message, EMAIL_FROM_ADDR, bcc=bcc_list)
        email.send()
