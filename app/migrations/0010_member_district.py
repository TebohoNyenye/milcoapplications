# Generated by Django 4.0.1 on 2022-02-09 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_member_accno_remove_member_bio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='district',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
