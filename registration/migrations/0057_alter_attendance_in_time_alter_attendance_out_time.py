# Generated by Django 5.1 on 2024-10-23 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0056_alter_attendance_attd_date_alter_attendance_in_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='in_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='out_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
