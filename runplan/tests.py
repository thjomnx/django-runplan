from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from runplan.models import Run

class AccessTest(TestCase):
    def test_http_raw_index(self):
        response = self.client.get(reverse('runplan.views.index'))
        self.assertEqual(response.status_code, 302)
        

    def test_http_raw_create(self):
        response = self.client.get(reverse('runplan.views.create'))
        self.assertEqual(response.status_code, 302)
    
    def test_http_raw_detail(self):
        u = User.objects.create_user('testuser', 'testuser@django.com', 'testpass')
        u.save()
        
        r = Run(author=u, meeting_date=timezone.now(), starting_point='sp', track_name='tn')
        r.save()
        
        response = self.client.get(reverse('runplan.views.detail', args=(r.id,)))
        self.assertEqual(response.status_code, 302)
