# Generated by Django 5.0 on 2024-01-03 03:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modul', '0002_remove_module_defaultget_remove_module_dilihat_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='biaya',
        ),
        migrations.RemoveField(
            model_name='module',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='module',
            name='mahkota',
        ),
    ]