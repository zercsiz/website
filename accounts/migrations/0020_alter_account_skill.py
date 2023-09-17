# Generated by Django 4.2.3 on 2023-09-17 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_alter_account_skill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='skill',
            field=models.CharField(blank=True, choices=[('زبان آلمانی', 'g'), ('زبان انگلیسی', 'e')], max_length=200, null=True, verbose_name='Skill'),
        ),
    ]
