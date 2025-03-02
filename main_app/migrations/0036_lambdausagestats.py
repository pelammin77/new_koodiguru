# Generated by Django 4.2.16 on 2025-01-16 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0035_remove_lambdausage_cost_usd_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LambdaUsageStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_executions', models.IntegerField(default=0)),
                ('last_execution', models.DateTimeField(blank=True, null=True)),
                ('executions_today', models.IntegerField(default=0)),
                ('last_execution_date', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Lambda Usage Statistics',
                'verbose_name_plural': 'Lambda Usage Statistics',
            },
        ),
    ]
