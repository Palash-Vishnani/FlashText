# Generated by Django 3.2.7 on 2022-06-19 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typingtest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstatistic',
            name='login_user',
            field=models.CharField(default='', max_length=25),
        ),
    ]