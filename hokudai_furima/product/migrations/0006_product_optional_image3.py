# Generated by Django 2.0.3 on 2018-03-28 16:51

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='optional_image3',
            field=versatileimagefield.fields.VersatileImageField(blank=True, upload_to='products/images/', verbose_name='Optional Image3'),
        ),
    ]