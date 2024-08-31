# Generated by Django 5.1 on 2024-08-31 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_rename_staff_mobile_number_mosque_imam_mobile_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mosque',
            name='district',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mosque',
            name='division',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mosque',
            name='imam_mobile_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='mosque',
            name='muazzin_mobile_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='mosque',
            name='muazzin_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mosque',
            name='thana',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mosque',
            name='village',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
