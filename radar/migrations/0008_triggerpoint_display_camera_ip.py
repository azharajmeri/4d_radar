# Generated by Django 5.0.3 on 2024-03-21 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radar', '0007_remove_radar_port_radar_host_ip'),
    ]

    operations = [
        migrations.CreateModel(
            name='TriggerPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display', models.IntegerField()),
                ('camera', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='display',
            name='camera_ip',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
