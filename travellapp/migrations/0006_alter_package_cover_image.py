# Generated by Django 4.0.3 on 2023-07-25 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travellapp', '0005_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='cover_image',
            field=models.ImageField(upload_to='Packages/Pictures/'),
        ),
    ]