# Generated by Django 4.1 on 2024-03-31 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0030_remove_user_level_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='level',
            field=models.IntegerField(default=0, verbose_name='Taso'),
        ),
    ]
