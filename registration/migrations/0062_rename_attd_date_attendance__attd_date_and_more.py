# Generated by Django 5.1 on 2024-10-25 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0061_alter_attendance_attd_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='attd_date',
            new_name='_attd_date',
        ),
        migrations.RenameField(
            model_name='attendance',
            old_name='in_time',
            new_name='_in_time',
        ),
        migrations.RenameField(
            model_name='attendance',
            old_name='out_time',
            new_name='_out_time',
        ),
    ]
