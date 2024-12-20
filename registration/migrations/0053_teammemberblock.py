# Generated by Django 5.1 on 2024-10-19 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0052_aboutusblock'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMemberBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='team_images/')),
                ('bio', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
