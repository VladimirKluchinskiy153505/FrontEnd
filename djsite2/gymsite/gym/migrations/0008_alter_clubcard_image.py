# Generated by Django 4.2.1 on 2023-09-10 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0007_remove_article_time_clubcard_image_alter_review_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubcard',
            name='image',
            field=models.ImageField(null=True, upload_to='photos/card_images'),
        ),
    ]
