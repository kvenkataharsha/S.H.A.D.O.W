# Generated by Django 2.2.7 on 2019-11-16 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20191116_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authority',
            name='Email_id',
            field=models.EmailField(default='shadow@gmail.com', max_length=254),
        ),
        migrations.AlterField(
            model_name='journalist',
            name='Email_id',
            field=models.EmailField(default='shadow@gmail.com', max_length=254),
        ),
    ]
