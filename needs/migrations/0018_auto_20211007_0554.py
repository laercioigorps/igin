# Generated by Django 3.2.5 on 2021-10-07 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('needs', '0017_auto_20211007_0554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='need',
            name='iconColor',
            field=models.CharField(default='', max_length=17, null=True),
        ),
        migrations.AlterField(
            model_name='need',
            name='iconName',
            field=models.CharField(default='', max_length=20, null=True),
        ),
    ]
