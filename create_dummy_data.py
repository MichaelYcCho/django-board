import os
import django
import sys
from pathlib import Path

# Django 설정
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "board_project.settings")
django.setup()

from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import random
import hashlib
from board_photo.models import PhotoBoard
from board_routine.models import RoutineBoard


def hash_password(password):
    """비밀번호를 해시화"""
    return hashlib.sha256(password.encode()).hexdigest()


def create_dummy_image(prefix="dummy"):
    """더미 이미지 생성"""
    color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    img = Image.new("RGB", (400, 300), color=color)

    img_io = BytesIO()
    img.save(img_io, format="JPEG", quality=85)
    img_io.seek(0)

    return ContentFile(img_io.read(), name=f"{prefix}_{random.randint(1000, 9999)}.jpg")


def create_photo_dummy_data():
    """사진 게시판 더미 데이터 생성"""
    print("사진 게시판 더미 데이터 생성 중...")

    # 기존 데이터 삭제
    PhotoBoard.objects.all().delete()

    for i in range(1, 101):
        photo = PhotoBoard.objects.create(
            title=f"사진 게시글 {i}번 - {random.choice(['멋진 풍경', '일상 사진', '여행 기록', '맛있는 음식', '귀여운 반려동물'])}",
            first_name=random.choice(
                ["민수", "지영", "성호", "은정", "준혁", "수빈", "태형", "혜진"]
            ),
            last_name=random.choice(["김", "이", "박", "최", "정", "강", "조", "윤"]),
            email=f"user{i}@example.com",
            password=hash_password("1234"),
            content=f"""이것은 {i}번째 사진 게시글입니다.

{random.choice([
    '오늘 찍은 멋진 사진을 공유합니다! 날씨가 정말 좋아서 산책하면서 찍었어요.',
    '맛있는 음식 사진입니다. 정말 맛있게 먹었답니다!',
    '여행 중에 찍은 사진이에요. 정말 아름다운 곳이었습니다.',
    '일상 속 소소한 행복을 담은 사진입니다.',
    '친구들과 함께 즐거운 시간을 보낸 기념사진이에요!'
])}

{random.choice([
    '여러분도 좋은 하루 보내세요!',
    '댓글로 의견 남겨주세요~',
    '좋아요 많이 눌러주세요!',
    '다음에 더 좋은 사진으로 찾아뵐게요!',
    '모두 행복한 하루 되세요!'
])}""",
            image=create_dummy_image("photo"),
        )

        if i % 10 == 0:
            print(f"사진 게시글 {i}개 생성 완료...")

    print("✅ 사진 게시판에 100개의 더미 데이터가 성공적으로 생성되었습니다!")


def create_routine_dummy_data():
    """루틴 게시판 더미 데이터 생성"""
    print("읽걷쓰 루틴 챌린지 더미 데이터 생성 중...")

    # 기존 데이터 삭제
    RoutineBoard.objects.all().delete()

    read_titles = [
        "오늘의 독서: 소설 완독!",
        "책 한 권 읽기 완료",
        "30분 독서 인증",
        "새로운 책 시작!",
        "도서관에서 책 읽기",
        "전자책 읽기 완료",
    ]

    walk_titles = [
        "아침 산책 30분 완료",
        "저녁 걷기 운동",
        "공원에서 걷기",
        "계단 오르기 운동",
        "산책로 걷기",
        "우산 들고 비 맞으며 걷기",
    ]

    write_titles = [
        "일기 쓰기 완료",
        "블로그 포스팅",
        "감사 일기 작성",
        "오늘의 소감문",
        "독서 감상문 작성",
        "하루 회고록",
    ]

    for i in range(1, 101):
        activity_type = random.choice(["read", "walk", "write"])

        if activity_type == "read":
            title = f"📚 {random.choice(read_titles)} - {i}일차"
            content = f"""읽걷쓰 루틴 챌린지 {i}일차 인증입니다!

📖 **읽기 활동**
오늘은 {random.choice(['소설', '에세이', '자기계발서', '시집', '만화책', '잡지'])}를 읽었습니다.
{random.choice(['30분', '1시간', '2시간', '45분'])} 동안 집중해서 읽었어요.

{random.choice([
    '정말 흥미진진한 내용이었습니다!',
    '많은 생각을 하게 되는 책이네요.',
    '다음 장이 궁금해서 시간 가는 줄 몰랐어요.',
    '새로운 지식을 얻을 수 있어서 좋았습니다.'
])}

내일도 꾸준히 읽어보겠습니다! 💪"""

        elif activity_type == "walk":
            title = f"🚶‍♀️ {random.choice(walk_titles)} - {i}일차"
            content = f"""읽걷쓰 루틴 챌린지 {i}일차 인증입니다!

🚶‍♂️ **걷기 활동**
오늘은 {random.choice(['공원', '산책로', '동네', '해변', '산', '강변'])}에서 걸었습니다.
총 {random.choice(['30분', '45분', '1시간', '20분'])} 동안 {random.choice(['3km', '5km', '2km', '4km'])} 걸었어요.

{random.choice([
    '날씨가 정말 좋아서 기분이 상쾌했습니다!',
    '걸으면서 많은 생각을 정리할 수 있었어요.',
    '운동 후 몸이 가벼워진 느낌입니다.',
    '자연을 보며 걸으니 스트레스가 해소되네요.'
])}

꾸준한 걷기로 건강을 챙기겠습니다! 🏃‍♀️"""

        else:  # write
            title = f"✍️ {random.choice(write_titles)} - {i}일차"
            content = f"""읽걷쓰 루틴 챌린지 {i}일차 인증입니다!

✍️ **쓰기 활동**
오늘은 {random.choice(['일기', '감상문', '블로그 글', '소감문', '편지', '시'])}를 썼습니다.
{random.choice(['20분', '30분', '45분', '1시간'])} 동안 집중해서 작성했어요.

{random.choice([
    '글을 쓰면서 하루를 정리할 수 있어서 좋았습니다.',
    '생각을 글로 표현하니 마음이 정리되네요.',
    '꾸준한 글쓰기로 표현력이 늘고 있는 것 같아요.',
    '오늘 있었던 일들을 되돌아보는 시간이었습니다.'
])}

내일도 좋은 글로 찾아뵐게요! ✨"""

        routine = RoutineBoard.objects.create(
            title=title,
            first_name=random.choice(
                ["민수", "지영", "성호", "은정", "준혁", "수빈", "태형", "혜진"]
            ),
            last_name=random.choice(["김", "이", "박", "최", "정", "강", "조", "윤"]),
            email=f"routine_user{i}@example.com",
            password=hash_password("1234"),
            content=content,
            image=(
                create_dummy_image("routine") if random.choice([True, False]) else None
            ),
        )

        if i % 10 == 0:
            print(f"루틴 챌린지 글 {i}개 생성 완료...")

    print(
        "✅ 읽걷쓰 루틴 챌린지 게시판에 100개의 더미 데이터가 성공적으로 생성되었습니다!"
    )


if __name__ == "__main__":
    print("🚀 더미 데이터 생성을 시작합니다...")

    try:
        create_photo_dummy_data()
        create_routine_dummy_data()
        print("\n🎉 모든 더미 데이터 생성이 완료되었습니다!")
        print("📝 총 200개의 게시글이 생성되었습니다 (각 게시판당 100개)")
        print("🔑 모든 더미 데이터의 비밀번호: 1234")

    except Exception as e:
        print(f"❌ 오류가 발생했습니다: {e}")
