# Generated by Django 4.0.5 on 2022-08-22 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0005_rename_isbn_issuedbook_bookid_remove_book_isbn'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuedbook',
            name='user',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
