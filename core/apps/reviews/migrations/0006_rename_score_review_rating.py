# Generated by Django 5.1.1 on 2024-09-19 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_alter_category_options_alter_genre_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='score',
            new_name='rating',
        ),
    ]
