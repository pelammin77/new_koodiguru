# Generated by Django 4.2.1 on 2023-10-02 20:45

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_tutorial_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
