# Generated by Django 3.2 on 2021-10-12 22:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hybrid_app', '0028_auto_20210615_0812'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='shared_with',
            new_name='shared_with_student_lists',
        ),
    ]
