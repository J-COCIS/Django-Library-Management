# Generated by Django 4.0.5 on 2022-08-10 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_alter_book_bookid_alter_issuedbook_issuedate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issuedbook',
            old_name='bookid',
            new_name='bookid2',
        ),
    ]
