# Generated by Django 3.2 on 2021-05-22 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hybrid_app', '0009_block_edit'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='image',
            field=models.ImageField(default='default.png', upload_to='hybrid_app/images'),
        ),
    ]
