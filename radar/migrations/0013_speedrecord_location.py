# Generated by Django 5.0.3 on 2024-03-24 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radar', '0012_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='speedrecord',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
