# Generated by Django 4.0.5 on 2023-07-21 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='discount_rate',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='tax_rate',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total',
            field=models.FloatField(blank=True),
        ),
    ]
