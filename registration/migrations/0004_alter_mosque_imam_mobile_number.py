# Generated by Django 5.1 on 2024-08-31 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_alter_mosque_district_alter_mosque_division_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mosque',
            name='imam_mobile_number',
            field=models.CharField(default=5, max_length=15),
            preserve_default=False,
        ),
    ]
