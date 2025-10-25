from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class firstTest(TestCase):
    def test_example(self):
        self.assertEqual(1 + 1, 2)
    
    def test_view_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)