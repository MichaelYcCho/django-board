from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from datetime import timedelta


def upload_to_routine(instance, filename):
    """읽걷쓰 루틴 챌린지 인증사진 업로드 경로 - S3의 read_walk_write_challenge 폴더에 저장"""
    import uuid
    import os

    # 파일 확장자 유지하면서 고유한 파일명 생성
    ext = filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    return f"read_walk_write_challenge/{unique_filename}"


class Like(models.Model):
    ip_address = models.GenericIPAddressField("IP 주소")
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    routine = models.ForeignKey('RoutineBoard', on_delete=models.CASCADE, related_name='likes')

    class Meta:
        verbose_name = "좋아요"
        verbose_name_plural = "좋아요"

    def __str__(self):
        return f"{self.ip_address} - {self.routine.title}"


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

    def can_like(self, ip_address):
        """해당 IP가 5분 이내에 좋아요를 누를 수 있는지 확인"""
        last_like = self.likes.filter(ip_address=ip_address).order_by('-created_at').first()
        if not last_like:
            return True
        return timezone.now() - last_like.created_at > timedelta(minutes=5)

    def get_like_count(self):
        """좋아요 수 반환"""
        return self.likes.count()
