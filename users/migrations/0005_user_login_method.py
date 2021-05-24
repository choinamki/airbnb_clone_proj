# Generated by Django 3.2.3 on 2021-05-24 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210523_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='login_method',
            field=models.CharField(choices=[('email', 'Email'), ('github', 'Github'), ('kakao', 'kakao')], default='email', max_length=50),
        ),
    ]
