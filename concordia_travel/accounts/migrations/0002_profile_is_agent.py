# Generated by Django 5.0.2 on 2024-02-26 17:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="is_agent",
            field=models.BooleanField(default=False),
        ),
    ]