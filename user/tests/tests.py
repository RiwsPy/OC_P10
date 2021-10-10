from django.test import TestCase
from django.contrib.auth.models import User
from django.urls.base import reverse

username = 'testuser'
email = 'loulou@test.com'
password = 'Pxâ76jjs1Ps'


class User_test(TestCase):
    def setUp(self):
        self.data = {
            'username': username,
            'email': email,
            'password': password,
        }
        self.user = User.objects.create_user(**self.data)

    def user_login(self):
        kwargs = self.data.copy()
        kwargs['password1'] = kwargs['password']
        response = self.client.post(reverse('login'), kwargs, follow=True)

        return response

    def test_create_user(self):
        self.assertEqual(self.user.username, username)
        self.assertEqual(self.user.email, email)
        self.assertTrue(self.user.is_authenticated)

    def test_login_page_status_code(self):
        response = self.client.get('/user/login/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')

    def test_account_page_status_code(self):
        response = self.user_login()
        response = self.client.get(reverse('account'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/account.html')

    def test_valid_user_login(self):
        response = self.user_login()
        self.assertTrue(response.context["user"].is_authenticated)

    def test_user_show_favorite_html(self):
        self.user_login()
        response = self.client.get(reverse('favorite'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogue/result.html')

    def test_false_user_login(self):
        data = {
            'username': username,
            'password1': 'qdoOiqfn{',
        }
        response = self.client.post(reverse('login'), data, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_user_connected_cannot_register(self):
        self.user_login()
        response = self.client.get(reverse('register'))

        self.assertRedirects(response, '/')


class User_without_auto_login(TestCase):
    def test_account(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)

    def test_favorite(self):
        response = self.client.get(reverse('favorite'))
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_register_user(self):
        data = {
            'username': 'Colette',
            'email': 'lovepetitpois@rat.com',
            'password1': password,
            'password2': password,
        }
        response = self.client.post(reverse('register'), data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, '/')

    def test_register_user_fail(self):
        data = {
            'username': 'Colette',
            'email': 'lovepetitpois@rat.com',
            'password1': password,
            'password2': password+'nope',
        }
        response = self.client.post(reverse('register'), data, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, 'user/register.html')
