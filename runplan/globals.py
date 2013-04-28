import datetime
import random
import string

datetime_format='%d.%m.%Y %H:%M'
meettime_threshold=datetime.timedelta(minutes=15)

def random_string(length=8, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(length))
