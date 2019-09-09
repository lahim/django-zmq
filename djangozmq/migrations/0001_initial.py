# Generated by Django 2.2.5 on 2019-09-09 23:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name='Modified on')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('status', models.IntegerField(default=0, verbose_name='Status')),
                ('error', models.CharField(blank=True, max_length=255, null=True, verbose_name='Error')),
                ('execution_time', models.FloatField(null=True, verbose_name='Execution time in seconds')),
                ('kwargs', models.CharField(blank=True, max_length=255, null=True, verbose_name='Task kwargs')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
