# Generated by Django 4.2.3 on 2024-05-28 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_remove_order_course_order_courseid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('p', 'pending'), ('c', 'complete'), ('i', 'incomplete')], default='incomplete', max_length=100, null=True),
        ),
    ]
