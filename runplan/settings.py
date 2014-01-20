import datetime

groupname='runplan-users'
noperm_target='/accounts/noperm/'

datetime_format='%d.%m.%Y %H:%M'
meettime_threshold=datetime.timedelta(minutes=15)
index_limit=50

email_from_addr = 'infobot@bochumrun.hopto.org'
email_subject_prefix = '[runplan] '

email_subject_templates = {
    'run.create': '$USER created new run',
    'run.edit': '$USER edited run',
    'run.cancel': '$USER canceled run',
    'run.attend': '$USER attends on run',
    'run.revoke': '$USER revokes for run',
    'run.transport.offer': '$USER offered new transport for run',
    'run.transport.edit': '$USER edited transport for run',
    'run.transport.cancel': '$USER canceled transport for run',
    'run.transport.takeseat': '$USER took seat on transport for run',
    'run.transport.freeseat': '$USER freed seat on transport for run',
}

email_body_templates = {
    'run.create': """
abc
""",
    'run.edit': """
def
""",
    'run.cancel': """
ghi
""",
    'run.attend': """
jkl
""",
    'run.revoke': """
mno
""",
    'run.transport.offer': """
pqr
""",
    'run.transport.edit': """
stu
""",
    'run.transport.cancel': """
vwx
""",
    'run.transport.takeseat': """
yzß
""",
    'run.transport.freeseat': """
äöü
""",
}
