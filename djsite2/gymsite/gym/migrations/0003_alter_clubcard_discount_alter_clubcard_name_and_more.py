# Generated by Django 4.2.1 on 2023-11-17 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0002_vacancy_image_vacancy_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubcard',
            name='discount',
            field=models.IntegerField(choices=[(1, 10), (2, 20), (3, 30), (4, 40)]),
        ),
        migrations.AlterField(
            model_name='clubcard',
            name='name',
            field=models.CharField(choices=[('B', 'Bronze'), ('S', 'Silver'), ('G', 'Gold'), ('D', 'Diamond')], max_length=10, verbose_name='ClubCard'),
        ),
        migrations.AlterField(
            model_name='master',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.TextField(max_length=300, null=True, verbose_name='QuestionAnswer'),
        ),
    ]