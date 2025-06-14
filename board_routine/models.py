from django.db import models
from django.core.validators import FileExtensionValidator


def upload_to_routine(instance, filename):
    """읽걷쓰 루틴 챌린지 인증사진 업로드 경로 - S3의 read_walk_write_challenge 폴더에 저장"""
    import uuid
    import os

    # 파일 확장자 유지하면서 고유한 파일명 생성
    ext = filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    return f"read_walk_write_challenge/{unique_filename}"


class RoutineBoard(models.Model):
    title = models.CharField("제목", max_length=200)
    first_name = models.CharField("이름", max_length=50)
    last_name = models.CharField("성", max_length=50)
    email = models.EmailField("이메일")
    password = models.CharField("비밀번호", max_length=128)
    content = models.TextField("내용")
    image = models.ImageField(
        "읽걷쓰 루틴 챌린지 인증사진",
        upload_to=upload_to_routine,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"])
        ],
        help_text="JPG, JPEG, PNG, GIF 파일만 업로드 가능합니다.",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField("작성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        verbose_name = "읽걷쓰 루틴 챌린지"
        verbose_name_plural = "읽걷쓰 루틴 챌린지"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def full_name(self):
        return f"{self.last_name}{self.first_name}"
