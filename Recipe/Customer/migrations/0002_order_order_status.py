# Generated by Django 4.2.1 on 2023-06-07 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(default='Requested', max_length=100),
        ),
    ]
