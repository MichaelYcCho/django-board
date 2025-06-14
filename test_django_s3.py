import os
import sys
import django
from pathlib import Path

# Django 설정
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "board_project.settings")

# Django 환경 설정
django.setup()

from django.core.files.base import ContentFile
from board_photo.models import PhotoBoard
from board_photo.views import hash_password
from PIL import Image
from io import BytesIO


# 테스트 이미지 생성
def create_test_image():
    """테스트용 이미지 생성"""
    img = Image.new("RGB", (400, 300), color=(255, 0, 0))  # 빨간색 이미지
    img_io = BytesIO()
    img.save(img_io, format="JPEG", quality=85)
    img_io.seek(0)
    return ContentFile(img_io.read(), name="test_s3_upload.jpg")


print("🧪 S3 업로드 테스트를 시작합니다...")

try:
    # 테스트 게시글 작성
    test_post = PhotoBoard.objects.create(
        title="S3 업로드 테스트",
        first_name="테스트",
        last_name="사용자",
        email="test@example.com",
        password=hash_password("1234"),
        content="S3에 이미지가 제대로 업로드되는지 테스트하는 게시글입니다.",
        image=create_test_image(),
    )

    print(f"✅ 테스트 게시글이 생성되었습니다! ID: {test_post.id}")
    print(f"📷 이미지 URL: {test_post.image.url}")
    print(f"📁 이미지 경로: {test_post.image.name}")

    # 이미지 URL이 S3 URL인지 확인
    if "estedu-img.s3" in test_post.image.url:
        print("🎉 S3 업로드가 성공적으로 작동하고 있습니다!")
    else:
        print("⚠️ 로컬 스토리지를 사용하고 있습니다.")

except Exception as e:
    print(f"❌ 오류가 발생했습니다: {e}")
    import traceback

    traceback.print_exc()
