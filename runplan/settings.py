from __future__ import unicode_literals

import datetime

from django.utils.translation import ugettext as _

groupname='runplan-users'
noperm_target='/accounts/noperm/'

datetime_format='%d.%m.%Y %H:%M'
meettime_threshold=datetime.timedelta(minutes=15)
index_limit=50

email_from_addr = 'infobot@thjom.de'

email_subject_prefix = _('[runplan] ')
email_subject_templates = {
    'run.create': _('%(user)s created new run %(run)s'),
    'run.edit': _('%(user)s edited run %(run)s'),
    'run.cancel': _('%(user)s canceled run %(run)s'),
    'run.attend': _('%(user)s attends on run %(run)s'),
    'run.revoke': _('%(user)s revokes for run %(run)s'),
    'run.transport.offer': _('%(user)s offered new transport for run %(run)s'),
    'run.transport.edit': _('%(user)s edited transport for run %(run)s'),
    'run.transport.cancel': _('%(user)s canceled transport for run %(run)s'),
    'run.transport.takeseat': _('%(user)s took seat on transport for run %(run)s'),
    'run.transport.freeseat': _('%(user)s freed seat on transport for run %(run)s'),
}

email_body_backlink = 'http://bochumrun.hopto.org'
email_body_header = ''
email_body_footer = _('This is an auto-generated e-mail - please do not respond!')
email_body_templates = {
    'run.create': _("""Link: %(link)s"""),
    'run.edit': _("""Link: %(link)s"""),
    'run.cancel': _("""Link: %(link)s"""),
    'run.attend': _("""Link: %(link)s"""),
    'run.revoke': _("""Link: %(link)s"""),
    'run.transport.offer': _("""Link: %(link)s"""),
    'run.transport.edit': _("""Link: %(link)s"""),
    'run.transport.cancel': _("""Link: %(link)s"""),
    'run.transport.takeseat': _("""Link: %(link)s"""),
    'run.transport.freeseat': _("""Link: %(link)s"""),
}
