# Generated by Django 3.2 on 2023-06-06 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('akademik', '0003_auto_20230605_1310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siswa',
            name='guru',
        ),
    ]
