# Generated by Django 5.1 on 2024-10-11 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0033_remove_qarrj_hasana_account_bank_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='qarrj_hasana_account',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='q_hasana_profile/'),
        ),
    ]
