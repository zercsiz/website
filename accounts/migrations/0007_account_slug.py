# Generated by Django 4.1.7 on 2023-04-17 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_account_description_account_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='slug',
            field=models.SlugField(max_length=300, null=True),
        ),
    ]