# Generated by Django 4.0.6 on 2022-09-01 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_work_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='pub_date',
            field=models.DateTimeField(verbose_name='date published'),
        ),
    ]