# Generated by Django 3.1.2 on 2020-10-17 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_bookinstance_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('Can mark as retuned', 'Set book as returned'),)},
        ),
    ]
