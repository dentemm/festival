# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-22 09:03
from __future__ import unicode_literals

from django.db import migrations
import home.models
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0031_auto_20160621_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='blog_content',
            field=wagtail.wagtailcore.fields.StreamField((('jeej', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('subtitle', wagtail.wagtailcore.blocks.CharBlock()), ('auteur', wagtail.wagtailcore.blocks.CharBlock())))), ('title', home.models.Heading1Block()), ('subtitle', home.models.Heading2Block()), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock(help_text='Geef de afbeelding een korte beschrijving', max_length=180, required=True))))), ('quote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.CharBlock(help_text='Geef hier een citaat in', max_length=150, required=True)), ('person', wagtail.wagtailcore.blocks.CharBlock(help_text='Van wie is dit citaat?', max_length=28, required=True))))), ('vid', wagtail.wagtailembeds.blocks.EmbedBlock()))),
        ),
    ]
