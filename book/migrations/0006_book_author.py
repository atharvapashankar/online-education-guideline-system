# Generated by Django 2.0.4 on 2019-03-12 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_remove_book_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.CharField(default='bala', max_length=200),
        ),
    ]
