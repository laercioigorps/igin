# Generated by Django 3.2.5 on 2021-07-14 08:50

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('needs', '0003_alter_goal_enddate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Iteration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
                ('date', models.DateField(default=datetime.datetime(2021, 7, 14, 8, 50, 0, 288785, tzinfo=utc))),
            ],
        ),
        migrations.AlterField(
            model_name='goal',
            name='endDate',
            field=models.DateField(default=datetime.datetime(2021, 7, 14, 8, 50, 0, 286783, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
                ('completed', models.BooleanField(default=False)),
                ('iteration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='needs.iteration')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='needs.step')),
            ],
        ),
    ]
