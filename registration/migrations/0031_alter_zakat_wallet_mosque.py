# Generated by Django 5.1 on 2024-10-07 21:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0030_alter_mosque_village'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zakat_wallet',
            name='mosque',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='registration.mosque'),
        ),
    ]
