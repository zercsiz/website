# Generated by Django 4.1.7 on 2023-03-16 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('start', models.TimeField(null=True)),
                ('end', models.TimeField(null=True)),
            ],
        ),
    ]