# Generated by Django 3.2.7 on 2022-06-20 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typingtest', '0003_rename_login_user_userstatistic_login_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('number', models.IntegerField()),
                ('feedback', models.TextField()),
            ],
        ),
    ]