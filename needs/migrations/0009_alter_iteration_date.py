# Generated by Django 3.2.5 on 2021-07-14 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('needs', '0008_auto_20210714_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iteration',
            name='date',
            field=models.DateField(blank=True),
        ),
    ]
