# Generated by Django 4.2.3 on 2023-09-17 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'pending'), ('complete', 'complete'), ('incomplete', 'incomplete')], default='incomplete', max_length=100, null=True),
        ),
    ]
