from __future__ import unicode_literals

from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse

from runplan.models import Settings
from runplan.settings import *
from runplan.utils import *

class Notification():
    email_query_mappings = {
        'run.create': {'emailon_newrun': True},
        'run.edit': {'emailon_modifiedrun': True},
        'run.cancel': {'emailon_canceledrun': True},
        'run.attend': {'emailon_runattend': True},
        'run.revoke': {'emailon_runrevoke': True},
        'run.transport.offer': {'emailon_transportoffer': True},
        'run.transport.edit': {'emailon_transportedit': True},
        'run.transport.cancel': {'emailon_transportcancel': True},
        'run.transport.takeseat': {'emailon_transportseattaken': True},
        'run.transport.freeseat': {'emailon_transportseatfreed': True},
    }
    
    def __init__(self, request, run, code):
        self.request = request
        self.run = run
        self.code = code
    
    def send(self):
        finalize_account(self.request.user)
        
        accounts = []
        kwargs = self.email_query_mappings[self.code]
        
        if self.code == 'run.create':
            for s in Settings.objects.filter(**kwargs):
                if s.account not in accounts:
                    accounts.append(s.account)
        else:
            observers = []
            
            for o in self.run.observation_set.all():
                if o.author not in observers:
                    observers.append(o.author)
            
            for s in Settings.objects.filter(**kwargs):
                if s.account not in accounts:
                    if s.emailon_observation == True:
                        if s.account in observers:
                            accounts.append(s.account)
                    else:
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
