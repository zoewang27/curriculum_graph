# Generated by Django 5.0.4 on 2024-05-31 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphvisualiztion', '0009_alter_trajectory_trajectory_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trajectory',
            name='trajectory_name',
            field=models.CharField(choices=[('Software Systems', 'Software Systems'), ('Modelbased Systems', 'Modelbased Systems'), ('Mathematics and Computer Science Theory', 'Mathematics and Computer Science Theory'), ('Data and Information Systems', 'Data and Information Systems'), ('Computer Systems', 'Computer Systems'), ('Academic Competences', 'Academic Competences')], max_length=100),
        ),
    ]
