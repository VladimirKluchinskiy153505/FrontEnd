# Generated by Django 4.2.1 on 2023-09-10 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0004_question_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(choices=[('swim', 'Swimming'), ('bobu', 'BoduBuilding'), ('yoga', 'Yoga'), ('dance', 'Dancing'), ('karate', 'Karate'), ('gymn', 'Gymnastics'), ('judo', 'Judo'), ('box', 'Boxing')], default='NoneSubject', max_length=20, verbose_name='SubjectName')),
            ],
        ),
    ]
