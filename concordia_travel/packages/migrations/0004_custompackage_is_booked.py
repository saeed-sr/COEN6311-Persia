# Generated by Django 5.0.2 on 2024-02-25 19:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("packages", "0003_custompackage"),
    ]

    operations = [
        migrations.AddField(
            model_name="custompackage",
            name="is_booked",
            field=models.BooleanField(default=False),
        ),
    ]
