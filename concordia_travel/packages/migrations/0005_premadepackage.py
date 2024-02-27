# Generated by Django 5.0.2 on 2024-02-27 00:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("packages", "0004_custompackage_is_booked"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PreMadePackage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "activities",
                    models.ManyToManyField(blank=True, to="packages.activity"),
                ),
                (
                    "agency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("flights", models.ManyToManyField(blank=True, to="packages.flight")),
                ("hotels", models.ManyToManyField(blank=True, to="packages.hotel")),
            ],
        ),
    ]
