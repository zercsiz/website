# Generated by Django 4.2.3 on 2023-09-18 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_order_teacher_alter_order_status_alter_order_student_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('complete', 'complete'), ('pending', 'pending'), ('incomplete', 'incomplete')], default='incomplete', max_length=100, null=True),
        ),
    ]