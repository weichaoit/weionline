# Generated by Django 2.0.5 on 2018-05-26 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20180525_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default='', upload_to='teacher/image/%Y/%m/%d', verbose_name='头像'),
        ),
    ]
