# Generated by Django 5.0.4 on 2024-05-31 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphvisualiztion', '0007_trajectory_level_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trajectory',
            name='objective_number',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
