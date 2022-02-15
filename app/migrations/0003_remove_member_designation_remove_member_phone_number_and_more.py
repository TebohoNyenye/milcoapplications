# Generated by Django 4.0.1 on 2022-02-08 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_employee_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='designation',
        ),
        migrations.RemoveField(
            model_name='member',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='member',
            name='email',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='first_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='last_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='username',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
