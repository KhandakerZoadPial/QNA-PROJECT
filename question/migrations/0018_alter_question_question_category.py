# Generated by Django 3.2.7 on 2021-09-18 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0017_fun'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.category'),
        ),
    ]
