# Generated by Django 5.0.6 on 2024-10-25 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0005_book_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='Borrowing_Price',
            field=models.IntegerField(),
        ),
    ]