# Generated by Django 5.0.6 on 2024-06-09 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='upload_resume',
            field=models.FileField(blank=True, null=True, upload_to='resume'),
        ),
    ]
