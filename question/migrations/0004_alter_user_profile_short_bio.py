# Generated by Django 3.2.7 on 2021-09-13 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0003_remove_question_type_of_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='short_bio',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
