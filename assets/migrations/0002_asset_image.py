# Generated by Django 3.2.4 on 2021-06-11 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='image',
            field=models.ImageField(default=None, upload_to='', verbose_name='Image'),
            preserve_default=False,
        ),
    ]
