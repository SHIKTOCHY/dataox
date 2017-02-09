# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-08 12:52
from __future__ import unicode_literals

import dirtyfields.dirtyfields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=2048, null=True)),
                ('index', models.IntegerField(null=True)),
                ('title', models.CharField(max_length=256)),
                ('file_path', models.TextField()),
                ('local_url', models.URLField()),
                ('mimetype', models.CharField(blank=True, max_length=64)),
                ('text', models.TextField()),
            ],
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vacancy_id', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=512)),
                ('location', models.CharField(max_length=1024)),
                ('organizationPart', models.CharField(blank=True, max_length=256)),
                ('formalOrganization', models.CharField(blank=True, max_length=256)),
                ('basedNear', models.CharField(blank=True, max_length=256)),
                ('description', models.TextField()),
                ('tags', models.TextField(blank=True)),
                ('category', models.TextField(blank=True, choices=[('academic', 'Academic'), ('support-technical', 'Support and Technical'), ('professional-management', 'Professional and Management'), ('research', 'Research'), ('temporary-staffing-service', 'Temporary Staffing Service')])),
                ('salary', models.CharField(blank=True, max_length=512)),
                ('salary_grade', models.CharField(blank=True, max_length=32)),
                ('salary_lower', models.PositiveIntegerField(blank=True, null=True)),
                ('salary_upper', models.PositiveIntegerField(blank=True, null=True)),
                ('salary_discretionary', models.PositiveIntegerField(blank=True, null=True)),
                ('contact_name', models.CharField(blank=True, max_length=128)),
                ('contact_email', models.CharField(blank=True, max_length=128)),
                ('contact_phone', models.CharField(blank=True, max_length=128)),
                ('url', models.URLField(blank=True, max_length=2048)),
                ('apply_url', models.URLField(blank=True, max_length=2048)),
                ('opening_date', models.CharField(max_length=25)),
                ('closing_date', models.CharField(blank=True, max_length=25, null=True)),
                ('internal', models.BooleanField()),
                ('last_checked', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'vacancies',
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.AddField(
            model_name='document',
            name='vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vacancy.Vacancy'),
        ),
    ]
