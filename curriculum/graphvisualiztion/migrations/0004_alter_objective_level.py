# Generated by Django 5.0.4 on 2024-05-31 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphvisualiztion', '0003_trajectories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objective',
            name='level',
            field=models.CharField(max_length=50),
        ),
    ]