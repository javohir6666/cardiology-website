# Generated by Django 5.2.1 on 2025-05-11 19:35

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_alter_menuitem_link_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagetranslation',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Page Content'),
        ),
    ]
