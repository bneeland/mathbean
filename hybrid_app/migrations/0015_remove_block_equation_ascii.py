# Generated by Django 3.2 on 2021-06-02 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hybrid_app', '0014_auto_20210528_2018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='equation_ascii',
        ),
    ]