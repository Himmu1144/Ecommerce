# Generated by Django 4.0.4 on 2022-06-17 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_product_category_product_images_product_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('msg_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=55)),
                ('email', models.CharField(max_length=50)),
                ('desc', models.CharField(max_length=2000)),
                ('phone', models.CharField(max_length=13)),
            ],
        ),
    ]
