# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-17 20:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0005_auto_20160304_1546'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vote',
            old_name='rating',
            new_name='score',
        ),
        migrations.RemoveField(
            model_name='score',
            name='score',
        ),
        migrations.RemoveField(
            model_name='score',
            name='votes',
        ),
        migrations.AddField(
            model_name='score',
            name='num_votes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='score',
            name='total_score',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='vote',
            name='overall_rating',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='ratings.Score'),
        ),
        migrations.AlterField(
            model_name='score',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_type_set_for_score', to='contenttypes.ContentType', verbose_name=b'content type'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_type_set_for_vote', to='contenttypes.ContentType', verbose_name=b'content type'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
