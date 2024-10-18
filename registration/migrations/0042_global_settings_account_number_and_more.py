# Generated by Django 5.1 on 2024-10-17 18:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0041_zakat_provider_transaction_screenshot_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='global_settings',
            name='account_number',
            field=models.CharField(default=0.0, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='global_settings',
            name='bank_name',
            field=models.CharField(default=0.0, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='global_settings',
            name='branch_name',
            field=models.CharField(default=datetime.datetime(2024, 10, 17, 18, 57, 30, 65308, tzinfo=datetime.timezone.utc), max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='global_settings',
            name='swift_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]