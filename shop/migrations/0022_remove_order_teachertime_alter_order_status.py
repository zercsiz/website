# Generated by Django 4.2.3 on 2023-09-17 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_order_teachertime_alter_order_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='teacherTime',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('complete', 'complete'), ('incomplete', 'incomplete'), ('pending', 'pending')], default='incomplete', max_length=100, null=True),
        ),
    ]
