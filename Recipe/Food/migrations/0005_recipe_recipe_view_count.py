# Generated by Django 4.2.1 on 2023-06-05 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Food', '0004_rename_recipe_catagory_recipe_recipe_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='recipe_view_count',
            field=models.IntegerField(default=1),
        ),
    ]
