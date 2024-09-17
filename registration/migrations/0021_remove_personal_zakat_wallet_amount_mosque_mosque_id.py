# Generated by Django 5.1 on 2024-09-17 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0020_zakat_receiver_personal_zakat_wallet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personal_zakat_wallet',
            name='amount',
        ),
        migrations.AddField(
            model_name='mosque',
            name='mosque_id',
            field=models.CharField(blank=True, max_length=10, unique=True),
        ),
    ]