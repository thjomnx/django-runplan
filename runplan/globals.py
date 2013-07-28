import datetime
import random
import string

groupname='runplan-users'
noperm_target='/accounts/noperm/'

datetime_format='%d.%m.%Y %H:%M'
meettime_threshold=datetime.timedelta(minutes=15)

index_limit=50

def random_string(length=8, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(length))
