# Generated by Django 2.0.4 on 2019-03-19 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_book_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.CharField(default='category', max_length=1000),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(default='pub', max_length=200),
        ),
    ]
