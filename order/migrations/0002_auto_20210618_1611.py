# Generated by Django 3.2.4 on 2021-06-18 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='color',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='size',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
