# Generated by Django 3.2.6 on 2021-09-20 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20210920_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='пароль)'),
        ),
    ]
