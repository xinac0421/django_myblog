# Generated by Django 2.1.3 on 2018-11-30 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20181122_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email_is_active',
            field=models.BooleanField(default=False, verbose_name='邮箱认证'),
        ),
    ]
