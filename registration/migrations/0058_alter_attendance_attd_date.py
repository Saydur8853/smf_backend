# Generated by Django 5.1 on 2024-10-23 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0057_alter_attendance_in_time_alter_attendance_out_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='attd_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]