# Generated by Django 5.2.3 on 2025-06-17 13:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("board_routine", "0002_alter_routineboard_options_alter_routineboard_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="Like",
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
                ("ip_address", models.GenericIPAddressField(verbose_name="IP 주소")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="생성일"),
                ),
                (
                    "routine",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="likes",
                        to="board_routine.routineboard",
                    ),
                ),
            ],
            options={
                "verbose_name": "좋아요",
                "verbose_name_plural": "좋아요",
            },
        ),
    ]
