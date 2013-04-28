from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.utils import timezone

from runplan.globals import *
from runplan.models import Run

fake_username='fakename'
fake_useremail='fake@fakehost.com'
fake_userpassword='fakepassword'

fake_run_starting_point=random_string(length=24)
fake_run_track_name=random_string(length=24)
fake_run_track_length=0.0

class ViewsTest(TestCase):
    def setUp(self):
        User.objects.create_user(fake_username, fake_useremail, fake_userpassword)
        self.client = Client()
    
    def test_view_index(self):
        response = self.client.get(reverse('runplan.views.index'))
        self.assertEqual(response.status_code, 302)
        
        self.client.login(username=fake_username, password=fake_userpassword)
        
        response = self.client.get(reverse('runplan.views.index'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_create(self):
        response = self.client.get(reverse('runplan.views.create'))
        self.assertEqual(response.status_code, 302)
        
        self.client.login(username=fake_username, password=fake_userpassword)
        
        response = self.client.get(reverse('runplan.views.create'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_detail(self):
        self.client.login(username=fake_username, password=fake_userpassword)
        
        u = User.objects.get(username=fake_username)
        r = Run(author=u,
                meeting_date=timezone.now(),
                starting_point=fake_run_starting_point,
                track_name=fake_run_track_name,
                track_length=fake_run_track_length)
        r.save()
        
        response = self.client.get(reverse('runplan.views.detail', args=(r.id,)))
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, fake_run_starting_point)
        self.assertContains(response, fake_run_track_name)
