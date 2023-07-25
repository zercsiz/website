from django.test import TestCase
from . import models
from . import forms

class modelsTest(TestCase):

    def setUp(self):
            self.account = models.Account.objects.create_user(email="ksourmi@gmail.com", password='ioioioio')
            self.request= {
                'email': "ksourmi@gmail.com",
                'password': "lksdjf"
            }
    def test_account_model_instance(self):
        self.assertTrue(isinstance(self.account, models.Account))

    def test_account_model_email_already_exists(self):
        try:
            user1 = self.account
            form = forms.RegistrationForm(self.request)
            if form.is_valid():
                user2 = form.save()
        except Exception as e:
            self.fail(e)
             
    def test_account_model_email_validate(self):
        try:
            form = forms.RegistrationForm(self.request)
            if form.is_valid():
                user1 = form.save()
        except Exception as e:
            self.fail(e)
                