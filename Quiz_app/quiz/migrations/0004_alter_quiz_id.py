# Generated by Django 3.2.12 on 2023-06-19 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_auto_20230618_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]