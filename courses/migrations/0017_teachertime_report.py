# Generated by Django 4.1.7 on 2023-04-12 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_alter_plantime_teacherplan'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachertime',
            name='report',
            field=models.TextField(null=True),
        ),
    ]