# Generated by Django 3.2 on 2021-05-29 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hybrid_app', '0013_auto_20210522_0933'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='equation_ascii',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='block',
            name='equation_latex',
            field=models.TextField(blank=True, null=True),
        ),
    ]