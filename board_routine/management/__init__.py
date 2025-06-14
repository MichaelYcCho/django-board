import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import random
from board_routine.models import RoutineBoard
from board_routine.utils import hash_password


class Command(BaseCommand):
    help = "읽걷쓰 루틴 챌린지 게시판에 더미 데이터 100개를 생성합니다."

    def handle(self, *args, **options):
        # 기존 데이터 삭제
        RoutineBoard.objects.all().delete()

        # 더미 이미지 생성 함수
        def create_dummy_image():
            # 읽걷쓰 테마 색상으로 이미지 생성
            colors = [
                (135, 206, 250),  # 하늘색 (걷기)
                (255, 182, 193),  # 핑크 (읽기)
                (144, 238, 144),  # 연두색 (쓰기)
                (255, 218, 185),  # 살구색
                (221, 160, 221),  # 자주색
            ]
            color = random.choice(colors)
            img = Image.new("RGB", (400, 300), color=color)

            # BytesIO로 이미지를 메모리에 저장
            img_io = BytesIO()
            img.save(img_io, format="JPEG", quality=85)
            img_io.seek(0)

            return ContentFile(
                img_io.read(), name=f"routine_proof_{random.randint(1000, 9999)}.jpg"
            )

        # 읽걷쓰 관련 제목과 내용
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

        # 더미 데이터 100개 생성
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
                last_name=random.choice(
                    ["김", "이", "박", "최", "정", "강", "조", "윤"]
                ),
                email=f"routine_user{i}@example.com",
                password=hash_password("1234"),  # 모든 더미 데이터의 비밀번호는 1234
                content=content,
                image=create_dummy_image() if random.choice([True, False]) else None,
            )

            if i % 10 == 0:
                self.stdout.write(f"루틴 챌린지 글 {i}개 생성 완료...")

        self.stdout.write(
            self.style.SUCCESS(
                f"읽걷쓰 루틴 챌린지 게시판에 100개의 더미 데이터가 성공적으로 생성되었습니다!"
            )
        )
