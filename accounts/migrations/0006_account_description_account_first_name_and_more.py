# Generated by Django 4.1.7 on 2023-04-01 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_account_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='description',
            field=models.TextField(max_length=1000, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='account',
            name='first_name',
            field=models.CharField(max_length=200, null=True, verbose_name='First Name'),
        ),
        migrations.AddField(
            model_name='account',
            name='last_name',
            field=models.CharField(max_length=200, null=True, verbose_name='Last Name'),
        ),
        migrations.AddField(
            model_name='account',
            name='skill',
            field=models.CharField(max_length=200, null=True, verbose_name='Skill'),
        ),
    ]
