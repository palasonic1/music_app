# Generated by Django 2.1.4 on 2018-12-16 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0002_auto_20181216_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artists',
            name='img_url',
            field=models.URLField(blank=True),
        ),
    ]
