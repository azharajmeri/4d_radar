# Generated by Django 5.0.3 on 2024-03-17 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radar', '0002_display'),
    ]

    operations = [
        migrations.AlterField(
            model_name='display',
            name='ip',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='display',
            name='port',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
