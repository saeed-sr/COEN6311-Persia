# Generated by Django 5.0.2 on 2024-03-21 04:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("booking", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="paid",
            field=models.BooleanField(default=False),
        ),
    ]
