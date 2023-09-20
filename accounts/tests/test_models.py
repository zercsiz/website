from django.test import TestCase
from accounts import models as accountsModels

class AccountModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        accountsModels.Account.objects.create(phone_number='09197858171', username="ksourmi", email="ksourmi@gmail.com")

    def setUp(self) -> None:
        self.account = accountsModels.Account.objects.get(id=1)

    def test_phone_number_label(self):
        field_label = self.account._meta.get_field('phone_number').verbose_name
        self.assertEqual(field_label, 'Phone Number')

    def test_username_label(self):
        field_label = self.account._meta.get_field('username').verbose_name
        self.assertEqual(field_label, "username")

    def test_phone_number_max_length(self):
        max_length = self.account._meta.get_field('phone_number').max_length
        self.assertEqual(max_length, 11)

    def test_username_max_length(self):
        max_length = self.account._meta.get_field('username').max_length
        self.assertEqual(max_length, 250)

    def test_superuser_str(self):
        self.account.is_superuser = True
        self.account.save()
        expected_object_name = f"Admin | {self.account.username} | {self.account.phone_number} | {self.account.email}"
        self.assertEqual(str(self.account), expected_object_name)

    def test_teacher_str(self):
        self.account.is_teacher = True
        self.account.is_student = True
        self.account.skill = 'german'
        self.account.save()
        expected_object_name = f"Teacher | {self.account.username} | {self.account.email} | {self.account.skill}"
        self.assertEqual(str(self.account), expected_object_name)

    def test_student_str(self):
        self.account.is_student = True
        self.account.first_name = "ali"
        self.account.last_name = "hamedani"
        self.account.save()
        expected_object_name = f"Student | {self.account.first_name} {self.account.last_name}"
        self.assertEqual(str(self.account), expected_object_name)

    def test_get_absolute_url(self):
        self.account.slug = "teacher-german-ali"
        self.assertEqual(self.account.get_absolute_url(), '/courses/teacher_details/1/teacher-german-ali/')