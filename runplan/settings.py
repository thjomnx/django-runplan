from __future__ import unicode_literals

import datetime

from django.utils.translation import ugettext as _

# Authentication and authorization
AUTH_GROUP_NAME='runplan-users'
NOPERM_TARGET='/accounts/noperm/'

# Query limits
RUNS_LIMIT=50
ACTIVITY_LIMIT=15
SHOUTS_LIMIT=10

# Timing thresholds
MEETTIME_THRESHOLD=datetime.timedelta(minutes=15)

# Email settings
EMAIL_FROM_ADDR = '<from address used for e-mail notification>'

EMAIL_SUBJECT_PREFIX = _('[runplan] ')
EMAIL_SUBJECT_TEMPLATES = {
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

EMAIL_BODY_BACKLINK = '<url used as link to site in e-mail body>'
EMAIL_BODY_HEADER = ''
EMAIL_BODY_FOOTER = _('This is an auto-generated e-mail - please do not respond!')
EMAIL_BODY_TEMPLATES = {
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

# Activity settings
ACTIVITY_TEXT_TEMPLATES = EMAIL_SUBJECT_TEMPLATES
