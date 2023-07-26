# Generated by Django 4.2.3 on 2023-07-25 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("travellapp", "0004_alter_news_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="Package",
            fields=[
                ("package_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("duration", models.CharField(max_length=100)),
                ("start_location", models.CharField(max_length=255)),
                ("end_location", models.CharField(max_length=255)),
                ("cover_image", models.URLField()),
                ("is_active", models.BooleanField(default=True)),
                ("start_date", models.DateField()),
                ("price", models.IntegerField()),
            ],
        ),
    ]
