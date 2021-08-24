from django.test import TestCase
from django.urls.base import reverse

# Create your tests here.

class HomePage(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

