# Generated by Django 4.2.3 on 2024-05-27 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('c', 'complete'), ('p', 'pending'), ('i', 'incomplete')], default='incomplete', max_length=100, null=True),
        ),
    ]
