# Generated by Django 4.1 on 2024-03-31 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0032_alter_user_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='points',
            field=models.IntegerField(default=0, verbose_name='Pisteet'),
        ),
    ]
