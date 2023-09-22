from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class TestAuthentication(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registrations(self):
        self.url = reverse('register')
        post_data = {
            'username': 'testusername',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }

        reponse = self.client.post(self.url, post_data)
        self.assertEqual(reponse.status_code, 302)
        self.assertEqual(User.objects.count(), 1)

    def test_login(self):
        self.url = reverse('user-login')
        self.user = User.objects.create(
            username='testusername',
            email='test@example.com',
            password='testpassword',
        )
        self.client.login(
            username='testusername',
            password='testpassword'
        )

        self.assertTrue(self.user.is_authenticated)

    def test_logout(self):
        self.url = reverse('user-logout')

        self.user = User.objects.create(
            username='testusername',
            email='test@example.com',
            password='testpassword',
        )

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
