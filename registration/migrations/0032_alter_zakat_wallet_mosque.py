# Generated by Django 5.1 on 2024-10-07 21:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0031_alter_zakat_wallet_mosque'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zakat_wallet',
            name='mosque',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='registration.mosque'),
        ),
    ]