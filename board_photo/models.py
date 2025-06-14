from django.db import models
from django.core.validators import FileExtensionValidator


def upload_to_photo(instance, filename):
    """사진 업로드 경로"""
    return f'board_photo/{filename}'


class PhotoBoard(models.Model):
    title = models.CharField('제목', max_length=200)
    first_name = models.CharField('이름', max_length=50)
    last_name = models.CharField('성', max_length=50)
    email = models.EmailField('이메일')
    password = models.CharField('비밀번호', max_length=128)
    content = models.TextField('내용')
    image = models.ImageField(
        '이미지', 
        upload_to=upload_to_photo,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
        help_text='JPG, JPEG, PNG, GIF 파일만 업로드 가능합니다.'
    )
    created_at = models.DateTimeField('작성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        verbose_name = '사진 게시판'
        verbose_name_plural = '사진 게시판'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def full_name(self):
        return f"{self.last_name}{self.first_name}"
