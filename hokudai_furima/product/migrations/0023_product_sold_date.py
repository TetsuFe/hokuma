# Generated by Django 2.0.3 on 2018-11-02 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_auto_20181102_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sold_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]