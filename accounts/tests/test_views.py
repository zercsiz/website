from django.test import TestCase
from django.urls import reverse
from accounts import models as accountsModels
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest
from django.contrib.auth import get_user_model


class UserRegistrationViewTest(TestCase):
    
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('accounts:user_registration'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('accounts:user_registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_view_creates_account_and_redirects_to_account_details(self):
        response = self.client.post(data={'email': 'ksourmi@gmail.com', 'password1':'yourtherichboy1'}, path='/accounts/register/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:account_details'))
        account = accountsModels.Account.objects.get(id=1)
        self.assertTrue(account)

    def test_view_authenticated_user_redirect_to_home(self):
        test_user = accountsModels.Account.objects.create(email='ksourmi@gmail.com', password=make_password("yourtherichboy1"), is_active=True)
        logged_in = self.client.login(email='ksourmi@gmail.com', password="yourtherichboy1")
        self.assertTrue(logged_in)
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home:home'))

    def test_view_form_in_context(self):
        response = self.client.get('/accounts/register/')
        self.assertTrue('form' in response.context )


class LoginViewTest(TestCase):

    def test_view_authenticated_user_redirect_to_home(self):
        test_user = accountsModels.Account.objects.create(email='ksourmi@gmail.com', password=make_password("yourtherichboy1"), is_active=True)
        logged_in = self.client.login(email='ksourmi@gmail.com', password="yourtherichboy1")
        self.assertTrue(logged_in)
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home:home'))

    def test_view_login_with_next(self):
        User = get_user_model()
        user = User.objects.create(email='ksourmi@gmail.com', password=make_password("yourtherichboy1"), is_active=True)
        
        response = self.client.post(path='/accounts/login/?next=/palette/', data={'email': 'ksourmi@gmail.com', 'password':'yourtherichboy1'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/palette/')
        self.assertTrue(user.is_authenticated)

    def test_view_login_without_next(self):
        account = accountsModels.Account.objects.create(email='ksourmi@gmail.com', password=make_password("yourtherichboy1"), is_active=True)
        response = self.client.post(path='/accounts/login/', data={'email': 'ksourmi@gmail.com', 'password':'yourtherichboy1'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home:home'))

class LogoutViewTest(TestCase):

    def test_view_unauthenticated_user_redirect_to_home(self):
        response = self.client.get(reverse('accounts:user_logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home:home'))

    def test_view_logouts_user_properly(self):
        User = get_user_model()
        user = User.objects.create(email='ksourmi@gmail.com', password=make_password("yourtherichboy1"), is_active=True)
        logged_in = self.client.login(email='ksourmi@gmail.com', password="yourtherichboy1")
        self.assertTrue(logged_in)
        self.assertTrue(user.is_authenticated)
        response = self.client.get('/accounts/logout/')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home:home'))
        # self.assertFalse(user.is_authenticated)