# Generated by Django 3.2.5 on 2021-10-20 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('needs', '0019_auto_20211007_0555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
