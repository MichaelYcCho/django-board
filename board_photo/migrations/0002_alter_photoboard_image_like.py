# Generated by Django 5.2.3 on 2025-06-17 14:06

import board_photo.models
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("board_photo", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="photoboard",
            name="image",
            field=models.ImageField(
                help_text="JPG, JPEG, PNG, GIF 파일만 업로드 가능합니다.",
                upload_to=board_photo.models.upload_to_photo,
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["jpg", "jpeg", "png", "gif"]
                    )
                ],
                verbose_name="사진",
            ),
        ),
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
                    "photo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="likes",
                        to="board_photo.photoboard",
                    ),
                ),
            ],
            options={
                "verbose_name": "좋아요",
                "verbose_name_plural": "좋아요",
            },
        ),
    ]
