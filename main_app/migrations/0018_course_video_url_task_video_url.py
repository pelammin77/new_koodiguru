# Generated by Django 4.1 on 2024-01-14 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0017_alter_course_creator_usertask_user_task_uniq_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='video_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='video_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
