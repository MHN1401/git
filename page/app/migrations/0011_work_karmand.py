# Generated by Django 4.0.6 on 2022-09-08 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_work_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='karmand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.karmand'),
        ),
    ]