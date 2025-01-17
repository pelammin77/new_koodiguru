# Generated by Django 4.2.16 on 2025-01-10 08:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0033_alter_user_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='LambdaUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('execution_time_ms', models.IntegerField(help_text='Execution time in milliseconds')),
                ('memory_used_mb', models.IntegerField(help_text='Memory used in megabytes')),
                ('cost_usd', models.DecimalField(blank=True, decimal_places=6, help_text='Cost in USD', max_digits=10, null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Lambda Usage',
                'verbose_name_plural': 'Lambda Usages',
                'ordering': ['-timestamp'],
            },
        ),
    ]
