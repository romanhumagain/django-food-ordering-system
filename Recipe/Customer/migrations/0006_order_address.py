# Generated by Django 4.2.1 on 2023-06-16 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0005_remove_order_customer_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
