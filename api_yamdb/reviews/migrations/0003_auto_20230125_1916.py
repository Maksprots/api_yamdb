# Generated by Django 3.2 on 2023-01-25 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20230125_1904'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='review',
            new_name='review_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='confirmation_code',
        ),
    ]