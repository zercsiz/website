# Generated by Django 4.2.3 on 2023-07-26 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_account_skill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='skill',
            field=models.CharField(blank=True, choices=[('زبان انگلیسی', 'e'), ('زبان آلمانی', 'g')], max_length=200, null=True, verbose_name='Skill'),
        ),
    ]
