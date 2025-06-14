# Django 게시판 프로젝트

이 프로젝트는 Django를 사용하여 만든 두 개의 게시판 시스템입니다.

## 기능

### 사진 게시판 (Photo Board)
- 이미지 업로드 기능
- 이름, 이메일, 비밀번호, 내용 입력
- CRUD 기능 (생성, 읽기, 수정, 삭제)
- 비밀번호 검증으로 수정/삭제 보안

### 루틴 게시판 (Routine Board)
- 선택적 이미지 업로드
- 이름, 이메일, 비밀번호, 내용 입력
- CRUD 기능 (생성, 읽기, 수정, 삭제)
- 비밀번호 검증으로 수정/삭제 보안

## 설치 및 실행

### 1. 가상환경 활성화
```bash
source venv/bin/activate
```

### 2. 패키지 설치 (이미 설치됨)
```bash
pip install django pillow
```

### 3. 데이터베이스 마이그레이션 (이미 완료됨)
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 슈퍼유저 생성 (이미 완료됨)
```bash
python manage.py createsuperuser
```

### 5. 서버 실행
```bash
python manage.py runserver
```

## 접속 URL

- **메인 페이지 (사진 게시판)**: http://127.0.0.1:8000/
- **사진 게시판**: http://127.0.0.1:8000/photo/
- **루틴 게시판**: http://127.0.0.1:8000/routine/
- **관리자 페이지**: http://127.0.0.1:8000/admin/

## 사용법

### 글 작성
1. 각 게시판의 "새 글 작성" 버튼 클릭
2. 제목, 이름(성/이름), 이메일, 비밀번호, 내용 입력
3. 이미지 업로드 (사진 게시판은 필수, 루틴 게시판은 선택)
4. "작성하기" 버튼 클릭

### 글 수정
1. 상세보기에서 "수정" 버튼 클릭
2. 비밀번호 입력하여 본인 확인
3. 내용 수정 후 "수정하기" 버튼 클릭

### 글 삭제
1. 상세보기에서 "삭제" 버튼 클릭
2. 비밀번호 입력하여 본인 확인
3. "삭제하기" 버튼 클릭

## 프로젝트 구조

```
django-board/
├── board_project/          # 메인 프로젝트 설정
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── board_photo/            # 사진 게시판 앱
│   ├── models.py          # PhotoBoard 모델
│   ├── views.py           # 뷰 함수들
│   ├── forms.py           # 폼 클래스들
│   ├── urls.py            # URL 패턴
│   └── admin.py           # 관리자 설정
├── board_routine/          # 루틴 게시판 앱
│   ├── models.py          # RoutineBoard 모델
│   ├── views.py           # 뷰 함수들
│   ├── forms.py           # 폼 클래스들
│   ├── urls.py            # URL 패턴
│   └── admin.py           # 관리자 설정
├── templates/              # HTML 템플릿
│   ├── base.html          # 기본 템플릿
│   ├── board_photo/       # 사진 게시판 템플릿
│   └── board_routine/     # 루틴 게시판 템플릿
├── media/                  # 업로드된 미디어 파일
└── manage.py
```

## 기능 상세

### 보안 기능
- 비밀번호 SHA256 해시화
- CSRF 보호
- 파일 확장자 검증 (JPG, JPEG, PNG, GIF만 허용)

### UI/UX 기능
- Bootstrap 5 사용한 반응형 디자인
- 파일 업로드 드래그 앤 드롭 지원
- 이미지 미리보기
- 페이지네이션
- 메시지 시스템 (성공/오류 알림)

### 관리자 기능
- Django Admin을 통한 게시글 관리
- 검색, 필터링 기능
- 일괄 작업 지원

## 개발자 정보

이 프로젝트는 Django 게시판 학습을 위해 제작되었습니다.
