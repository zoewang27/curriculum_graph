# Generated by Django 5.0.4 on 2024-06-08 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphvisualiztion', '0017_course_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='year',
            field=models.IntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3')], null=True),
        ),
    ]