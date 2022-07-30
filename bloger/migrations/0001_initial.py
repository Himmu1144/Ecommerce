# Generated by Django 4.0.4 on 2022-07-23 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blogpost',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=500)),
                ('content', models.CharField(default='', max_length=5000)),
                ('image', models.ImageField(upload_to='blog/images')),
                ('date', models.DateField()),
            ],
        ),
    ]
