from django.test import TestCase
from accounts import forms as accountsForms
from accounts import models as accountsModels

class RegistrationFormTest(TestCase):

    # def setUp(self):
    #     self.form = accountsForms.RegistrationForm(data={'email':"ksourmi@gmail.com", 'password1':"yourtherichboy"})

    def test_registration_form_email_label(self):
        self.form = accountsForms.RegistrationForm(data={'email':"ksourmi@gmail.com", 'password1':"yourtherichboy"})
        self.assertTrue(self.form.fields['email'].label is None or self.form.fields['email'].label == '')

    def test_registration_form_email_exists(self):
        accountsModels.Account.objects.create(phone_number='09197858171', username="ksourmi", email="ksourmi@gmail.com")

        self.form = accountsForms.RegistrationForm(data={'email':"ksourmi@gmail.com", 'password1':"yourtherichboy"})

        self.assertFalse(self.form.is_valid())

    def test_registration_form_invalid_email_without_dot(self):
        #giving the form invalid email without dot
        self.form = accountsForms.RegistrationForm(data={'email':"ksourmi@gmailcom", 'password1':"yourtherichboy"})
        self.assertFalse(self.form.is_valid())

    def test_registration_form_invalid_email_without_atsign(self):
        #giving the form invalid email without atsign
        self.form = accountsForms.RegistrationForm(data={'email':"ksourmigmail.com", 'password1':"yourtherichboy"})
        self.assertFalse(self.form.is_valid())

    def test_registration_form_password_under_8_chars_length(self):
        self.form = accountsForms.RegistrationForm(data={'email':"ksourmi@gmail.com", 'password1':"yyyyyyy"})
        self.assertFalse(self.form.is_valid())

    def test_registration_form_password_without_numbers(self):
        self.form = accountsForms.RegistrationForm(data={'email':"ksourmi@gmail.com", 'password1':"yyyyyyyyy"})
        self.assertFalse(self.form.is_valid())

    def test_registration_form_password_with_spaces(self):
        self.form = accountsForms.RegistrationForm(data={'email':"ksourmi@gmail.com", 'password1':"yyyy yyyyy"})
        self.assertFalse(self.form.is_valid())

    def test_registration_form_valid_password(self):
        self.form = accountsForms.RegistrationForm(data={'email':"ksourmi@gmail.com", 'password1':"hjoiuy7uih"})
        self.assertTrue(self.form.is_valid())


    def test_registration_form_password_saved_after_registration(self):
        self.form = accountsForms.RegistrationForm(data={'email':"ksourmi@gmail.com", 'password1':"hjoiuy7uih"})
        self.form.save()
        account = accountsModels.Account.objects.get(id=1)
        self.assertTrue(account.password)


class UserLoginFormTest(TestCase):
    def test_login_form_user_deos_not_exist(self):
        form = accountsForms.UserLoginForm(data={'email':"ksourmi@gmail.com", 'password':"hjoiuy7uih"})
        self.assertFormError(form=form, errors=['نام کاربری یا رمز عبور اشتباه است.'], field=None)