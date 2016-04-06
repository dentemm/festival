# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-06 17:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0028_merge'),
        ('taggit', '0002_auto_20150616_2121'),
        ('wagtailimages', '0012_copy_image_permissions_to_collections'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=40, verbose_name='stad')),
                ('postal_code', models.CharField(max_length=8, null=True, verbose_name='postcode')),
                ('street', models.CharField(max_length=40, null=True, verbose_name='straat')),
                ('number', models.CharField(max_length=8, null=True, verbose_name='nummer')),
                ('country', django_countries.fields.CountryField(default='BE', max_length=2, null=True, verbose_name='land')),
            ],
            options={
                'verbose_name': 'adres',
                'verbose_name_plural': 'adressen',
            },
        ),
        migrations.CreateModel(
            name='FestivalImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_primary', models.BooleanField(default=False, verbose_name='hoofdafbeelding')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.Image', verbose_name='afbeelding')),
            ],
        ),
        migrations.CreateModel(
            name='FestivalIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='FestivalLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FestivalPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('name', models.CharField(default='', max_length=40, unique=True, verbose_name='Festival naam')),
                ('description', wagtail.wagtailcore.fields.RichTextField(blank=True, default='', verbose_name='Festival promo tekst')),
                ('date', models.DateField(null=True, verbose_name='Festival datum')),
                ('duration', models.PositiveIntegerField(default=1, verbose_name='Duur (# dagen)')),
                ('website', models.URLField(blank=True, max_length=120, null=True)),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'Festival',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='FestivalPageRateableAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=27)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Beoordeelbaar kenmerk',
                'verbose_name_plural': 'Beoordeelbare kenmerken',
            },
        ),
        migrations.CreateModel(
            name='FestivalPageRatebleAttributeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='rateable_attributes', to='home.FestivalPage')),
                ('rateable_attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='home.FestivalPageRateableAttribute', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FestivalPageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='home.FestivalPage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_festivalpagetag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.wagtailcore.fields.StreamField((('carousel', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('caption', wagtail.wagtailcore.blocks.TextBlock(required=False)))), icon='image', template='home/blocks/carousel.html')),), null=True)),
            ],
            options={
                'verbose_name': 'Startpagina',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=28)),
                ('longitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='location', to='home.Address', verbose_name='adres')),
            ],
            options={
                'verbose_name': 'locatie',
                'verbose_name_plural': 'locaties',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=28, verbose_name='voornaam')),
                ('last_name', models.CharField(max_length=64, verbose_name='familienaam')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='email adres')),
                ('phone', models.CharField(max_length=28, null=True, verbose_name='telefoonnummer')),
            ],
            options={
                'ordering': ['last_name'],
                'verbose_name': 'persoon',
                'verbose_name_plural': 'personen',
            },
        ),
        migrations.AddField(
            model_name='festivalpage',
            name='contact_person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='festivals', to='home.Person'),
        ),
        migrations.AddField(
            model_name='festivalpage',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='festivals', to='home.Location'),
        ),
        migrations.AddField(
            model_name='festivalpage',
            name='main_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='festivalpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='home.FestivalPageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='festivallocation',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Location'),
        ),
        migrations.AddField(
            model_name='festivallocation',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='home.FestivalPage'),
        ),
        migrations.AddField(
            model_name='festivalimage',
            name='page',
            field=modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='home.FestivalPage'),
        ),
    ]
