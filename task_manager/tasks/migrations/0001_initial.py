# Generated by Django 5.2.3 on 2025-07-10 17:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('labels', '0001_initial'),
        ('statuses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='authored_tasks', to=settings.AUTH_USER_MODEL)),
                ('executor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='executed_tasks', to=settings.AUTH_USER_MODEL)),
                ('labels', models.ManyToManyField(blank=True, to='labels.label')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to='statuses.status')),
            ],
        ),
    ]
