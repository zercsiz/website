# Generated by Django 4.2.3 on 2023-09-17 14:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0013_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='sessions_number',
            field=models.IntegerField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('incomplete', 'incomplete'), ('pending', 'pending'), ('complete', 'complete')], default='incomplete', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_orders', to=settings.AUTH_USER_MODEL),
        ),
    ]
