# Generated by Django 4.1.7 on 2023-03-11 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funkdata', '0011_alter_functiontype_unique_function_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='functionall',
            name='syntax',
            field=models.CharField(max_length=64),
        ),
        migrations.DeleteModel(
            name='FunctionData',
        ),
    ]
