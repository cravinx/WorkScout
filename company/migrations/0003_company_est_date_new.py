# Generated by Django 5.0.6 on 2024-10-09 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='est_date_new',
            field=models.DateField(blank=True, null=True),
        ),
    ]
