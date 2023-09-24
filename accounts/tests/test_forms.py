from django.test import TestCase
from accounts import forms as accountsForms
from accounts import models as accountsModels
from django.http import HttpRequest

class RegistrationFormTest(TestCase):

    def test_registration_form_email_label(self):
        form = accountsForms.RegistrationForm(data={'email':"ksourmi@gmail.com", 'password1':"yourtherichboy"})
        self.assertTrue(form.fields['email'].label is None or form.fields['email'].label == '')

    def test_registration_form_email_exists(self):
        accountsModels.Account.objects.create(phone_number='09197858171', username="ksourmi", email="ksourmi@gmail.com")

        form = accountsForms.RegistrationForm(data={'email':"ksourmi@gmail.com", 'password1':"yourtherichboy"})

        self.assertFalse(form.is_valid())

    def test_registration_form_invalid_email_without_dot(self):
        #giving the form invalid email without dot
        form = accountsForms.RegistrationForm(data={'email':"ksourmi@gmailcom", 'password1':"yourtherichboy"})
        self.assertFalse(form.is_valid())

    def test_registration_form_invalid_email_without_atsign(self):
        #giving the form invalid email without atsign
        form = accountsForms.RegistrationForm(data={'email':"ksourmigmail.com", 'password1':"yourtherichboy"})
        self.assertFalse(form.is_valid())

    def test_registration_form_password_under_8_chars_length(self):
        form = accountsForms.RegistrationForm(data={'email':"ksourmi@gmail.com", 'password1':"yyyyyyy"})
        self.assertFalse(form.is_valid())

    def test_registration_form_password_without_numbers(self):
        form = accountsForms.RegistrationForm(data={'email':"ksourmi@gmail.com", 'password1':"yyyyyyyyy"})
        self.assertFalse(form.is_valid())

    def test_registration_form_password_with_spaces(self):
        form = accountsForms.RegistrationForm(data={'email':"ksourmi@gmail.com", 'password1':"yyyy yyyyy"})
        self.assertFalse(form.is_valid())

    def test_registration_form_valid_password(self):
        form = accountsForms.RegistrationForm(data={'email':"ksourmi@gmail.com", 'password1':"hjoiuy7uih"})
        self.assertTrue(form.is_valid())


    def test_registration_form_password_saved_after_registration(self):
        self.form = accountsForms.RegistrationForm(data={'email':"ksourmi@gmail.com", 'password1':"hjoiuy7uih"})
        self.form.save()
        account = accountsModels.Account.objects.get(id=1)
        self.assertTrue(account.password)


class UserLoginFormTest(TestCase):
    def test_login_form_user_deos_not_exist(self):
        form = accountsForms.UserLoginForm(data={'email':"ksourmi@gmail.com", 'password':"hjoiuy7uih"})
        self.assertFormError(form=form, errors=['نام کاربری یا رمز عبور اشتباه است.'], field=None)



class AccountEditFormTest(TestCase):

    def test_AccountEditForm_user_not_teacher_skill_and_description_fields_pop(self):
        account = accountsModels.Account.objects.create(phone_number='09197858171', username="ksourmi", email="ksourmi@gmail.com", is_teacher=False)
        account.save()
        form = accountsForms.AccountEditForm(instance=account)

        self.assertNotIn('skill', form.fields)
        self.assertNotIn('description', form.fields)

    def test_AccountEditForm_user_is_teacher_form_with_skill_and_description_fields(self):
        account = accountsModels.Account.objects.create(phone_number='09197858171', username="ksourmi", email="ksourmi@gmail.com", is_teacher=True)
        account.save()
        form = accountsForms.AccountEditForm(instance=account)

        self.assertIn('skill', form.fields)
        self.assertIn('description', form.fields)

    def test_AccountEditForm_username_already_exists(self):
        accountsModels.Account.objects.create(phone_number='09197858171', username="ksourmi", email="ksourmi@gmail.com", is_teacher=True)
        form = accountsForms.AccountEditForm(data={'username': 'ksourmi', 'email': 'test@gmail.com'})
        self.assertFalse(form.is_valid())
        self.assertFormError(form=form, errors=['Username "ksourmi" already exists!'], field='username')

    def test_AccountEditForm_phone_number_already_exists(self):
        accountsModels.Account.objects.create(phone_number='09197858171', username="ksourmi", email="ksourmi@gmail.com", is_teacher=True)
        form = accountsForms.AccountEditForm(data={'phone_number': '09197858171', 'email': 'test@gmail.com'})
        self.assertFalse(form.is_valid())
        self.assertFormError(form=form, errors=['Phone number "09197858171" already exists!'], field='phone_number')

    def test_AccountEditForm_email_already_exists(self):
        accountsModels.Account.objects.create(phone_number='09197858171', username="ksourmi", email="ksourmi@gmail.com", is_teacher=True)
        form = accountsForms.AccountEditForm(data={'username': 'usernametest', 'email': 'ksourmi@gmail.com'})
        self.assertFalse(form.is_valid())
        self.assertFormError(form=form, errors=['Email "ksourmi@gmail.com" already exists!'], field='email')

