# Generated by Django 4.2.1 on 2023-06-21 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Food', '0005_recipe_recipe_view_count'),
        ('Customer', '0010_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Food.recipe'),
        ),
    ]
