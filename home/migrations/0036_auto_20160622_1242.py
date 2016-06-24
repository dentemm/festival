# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-22 10:42
from __future__ import unicode_literals

from django.db import migrations
import home.models
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0035_auto_20160622_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='blog_content',
            field=wagtail.wagtailcore.fields.StreamField((('blog_title', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('auteur', wagtail.wagtailcore.blocks.CharBlock())), help_text='Dit is de titel van het artikel, voorzien van een afbeelding')), ('subtitle', home.models.Heading2Block()), ('video', wagtail.wagtailcore.blocks.StructBlock((('link', wagtail.wagtailembeds.blocks.EmbedBlock(classname='block-background', label='URL van video', required=True)), ('titel', wagtail.wagtailcore.blocks.CharBlock(label='Titel', required=True)), ('desc', wagtail.wagtailcore.blocks.CharBlock(label='Beschrijving van video, optioneel', required=False))))), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock(help_text='Geef de afbeelding een korte beschrijving', max_length=180, required=True))))), ('quote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.CharBlock(help_text='Geef hier een citaat in', label='Citaat', max_length=150, required=True)), ('person', wagtail.wagtailcore.blocks.CharBlock(help_text='Van wie is dit citaat?', label='Auteur', max_length=28, required=True))))), ('vid', wagtail.wagtailembeds.blocks.EmbedBlock()))),
        ),
    ]
