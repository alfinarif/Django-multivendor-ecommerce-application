# Generated by Django 3.2.4 on 2021-06-17 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_variationvalue_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='variationvalue',
            name='price',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='variationvalue',
            name='variation',
            field=models.CharField(choices=[('size', 'size'), ('color', 'color')], max_length=100),
        ),
        migrations.DeleteModel(
            name='Variation',
        ),
    ]