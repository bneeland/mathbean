# Generated by Django 3.2 on 2021-06-11 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hybrid_app', '0019_document_max_block_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='max_block_order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]