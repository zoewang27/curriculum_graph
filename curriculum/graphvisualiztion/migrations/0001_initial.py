# Generated by Django 5.0.4 on 2024-05-30 22:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.IntegerField(primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=255)),
                ('lecturer', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('course_category', models.CharField(choices=[('C', 'Compulsory'), ('E', 'Elective')], default='C', max_length=1)),
                ('year', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3')], default=1)),
                ('period', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('level', models.IntegerField()),
                ('related_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='objectives', to='graphvisualiztion.course')),
            ],
        ),
    ]
