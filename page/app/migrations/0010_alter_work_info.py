# Generated by Django 4.0.6 on 2022-09-08 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_karmand_karfarma'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='info',
            field=models.CharField(max_length=300),
        ),
    ]