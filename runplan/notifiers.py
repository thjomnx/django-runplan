from __future__ import unicode_literals

from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse

from runplan.models import Settings
from runplan.settings import *
from runplan.utils import *

class Notification():
    email_query_mappings = {
        'run.create': {'field': 'emailon_newrun', 'value': True},
        'run.edit': {'field': 'emailon_modifiedrun', 'value': True},
        'run.cancel': {'field': 'emailon_canceledrun', 'value': True},
        'run.attend': {'field': 'emailon_runattend', 'value': True},
        'run.revoke': {'field': 'emailon_runrevoke', 'value': True},
        'run.transport.offer': {'field': 'emailon_transportoffer', 'value': True},
        'run.transport.edit': {'field': 'emailon_transportedit', 'value': True},
        'run.transport.cancel': {'field': 'emailon_transportcancel', 'value': True},
        'run.transport.takeseat': {'field': 'emailon_transportseattaken', 'value': True},
        'run.transport.freeseat': {'field': 'emailon_transportseatfreed', 'value': True},
    }
    
    def __init__(self, request, run, code):
        self.request = request
        self.run = run
        self.code = code
    
    def send(self):
        finalize_account(self.request.user)
        
        observers = []
        accounts = []
        
        for o in self.run.observation_set.all():
            if o.author not in accounts:
                observers.append(o.author)
                accounts.append(o.author)
        
        kwargs = {}
        
        for k, v in self.email_query_mappings.items():
            if self.code == k:
                kwargs[v['field']] = v['value']
                
                for s in Settings.objects.filter(**kwargs):
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
