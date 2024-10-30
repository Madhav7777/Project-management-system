# Generated by Django 4.0.6 on 2024-10-29 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprojectapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='priority',
            field=models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], db_column='priority', max_length=64),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='status',
            field=models.CharField(choices=[('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Done', 'Done')], db_column='status', max_length=64),
        ),
    ]