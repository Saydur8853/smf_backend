# Generated by Django 5.1 on 2024-10-11 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0034_qarrj_hasana_account_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qarrj_hasana_account',
            name='email',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
