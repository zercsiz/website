from django.test import TestCase
from django.urls import reverse
from accounts import models as accountsModels
from django.contrib.auth.hashers import make_password


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