# Generated by Django 3.2.7 on 2021-09-15 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0013_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
