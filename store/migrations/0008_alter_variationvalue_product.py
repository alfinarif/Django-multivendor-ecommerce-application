# Generated by Django 3.2.4 on 2021-06-18 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20210617_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variationvalue',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variation', to='store.product'),
        ),
    ]
