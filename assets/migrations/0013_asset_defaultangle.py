# Generated by Django 3.2.4 on 2021-07-28 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0012_auto_20210727_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='defaultAngle',
            field=models.IntegerField(default=0, verbose_name='defaultAngle'),
        ),
    ]
