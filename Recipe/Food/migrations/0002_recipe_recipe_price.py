# Generated by Django 4.2.1 on 2023-06-03 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Food', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='recipe_price',
            field=models.IntegerField(default=0),
        ),
    ]
