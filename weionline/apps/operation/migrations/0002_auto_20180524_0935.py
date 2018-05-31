# Generated by Django 2.0.5 on 2018-05-24 09:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecomment',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='userask',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='usercourse',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='学习时间'),
        ),
        migrations.AlterField(
            model_name='userfavorite',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='收藏时间'),
        ),
        migrations.AlterField(
            model_name='usermessage',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='收藏时间'),
        ),
    ]