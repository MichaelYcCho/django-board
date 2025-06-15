#!/bin/bash

# EC2 Django 프로젝트 배포 스크립트
set -e

echo "🚀 Django 프로젝트 배포를 시작합니다..."

# 프로젝트 디렉토리
PROJECT_DIR="/home/ubuntu/django-board"
REPO_URL="https://github.com/MichaelYcCho/django-board.git"  # 실제 GitHub 저장소 URL로 변경

# # 시스템 업데이트
# echo "📦 시스템 패키지 업데이트 중..."
# sudo apt update && sudo apt upgrade -y

# # 필수 패키지 설치
# echo "📦 필수 패키지 설치 중..."
# sudo apt install -y python3 python3-pip python3-venv nginx git

# # 프로젝트 디렉토리 생성
# echo "📁 프로젝트 디렉토리 설정 중..."
# sudo mkdir -p $PROJECT_DIR
# sudo chown ubuntu:ubuntu $PROJECT_DIR

# Git 저장소 클론 또는 업데이트
if [ -d "$PROJECT_DIR/.git" ]; then
    echo "🔄 기존 프로젝트 업데이트 중..."
    cd $PROJECT_DIR
    git pull origin main
else
    echo "📥 프로젝트 복제 중..."
    git clone $REPO_URL $PROJECT_DIR
    cd $PROJECT_DIR
fi

# 가상환경 생성 및 활성화
echo "🐍 Python 가상환경 설정 중..."
#python3 -m venv venv
source venv/bin/activate

# 의존성 설치
echo "📦 Python 패키지 설치 중..."
pip install --upgrade pip
pip install -r requirements-prod.txt

# .env파일 수동으로 만들어야함

# Django 설정
echo "⚙️  Django 설정 중..."
export DJANGO_SETTINGS_MODULE=board_project.settings_prod
python manage.py collectstatic --noinput
python manage.py migrate

# 로그 디렉토리 생성
echo "📋 로그 디렉토리 설정 중..."
mkdir -p $PROJECT_DIR/logs
sudo mkdir -p /var/log/gunicorn
sudo chown ubuntu:ubuntu /var/log/gunicorn

# Gunicorn 시스템 서비스 설정
echo "🔧 Gunicorn 서비스 설정 중..."
sudo tee /etc/systemd/system/django-board.service > /dev/null << EOF
[Unit]
Description=Django Board Gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --config $PROJECT_DIR/gunicorn.conf.py board_project.wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Nginx 설정
echo "🌐 Nginx 설정 중..."
sudo cp nginx.conf /etc/nginx/sites-available/django-board
sudo ln -sf /etc/nginx/sites-available/django-board /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Nginx 설정 문법 검사
echo "🔍 Nginx 설정 검사 중..."
sudo nginx -t

# 서비스 시작/재시작
echo "🚀 서비스 시작 중..."
sudo systemctl daemon-reload

# Django 애플리케이션 재시작 (설정 변경사항 반영)
sudo systemctl enable django-board
if sudo systemctl is-active --quiet django-board; then
    echo "🔄 Django 서비스 재시작 중..."
    sudo systemctl restart django-board
else
    echo "🆕 Django 서비스 시작 중..."
    sudo systemctl start django-board
fi

# Nginx 재시작 (설정 변경사항 반영)
sudo systemctl enable nginx
if sudo systemctl is-active --quiet nginx; then
    echo "🔄 Nginx 재시작 중..."
    sudo systemctl reload nginx  # reload는 restart보다 빠름
else
    echo "🆕 Nginx 시작 중..."
    sudo systemctl start nginx
fi

# 서비스 상태 확인
echo "📊 서비스 상태 확인 중..."
sleep 2  # 서비스 시작 대기

if sudo systemctl is-active --quiet django-board; then
    echo "✅ Django 서비스: 정상"
else
    echo "❌ Django 서비스: 오류"
    sudo systemctl status django-board --no-pager -l
fi

if sudo systemctl is-active --quiet nginx; then
    echo "✅ Nginx 서비스: 정상"
else
    echo "❌ Nginx 서비스: 오류"
    sudo systemctl status nginx --no-pager -l
fi

# 포트 확인
echo "🔌 포트 확인 중..."
if sudo netstat -tlnp | grep :80 > /dev/null; then
    echo "✅ 포트 80: 열림"
else
    echo "❌ 포트 80: 닫힘"
fi

if sudo netstat -tlnp | grep :8000 > /dev/null; then
    echo "✅ 포트 8000: 열림"
else
    echo "❌ 포트 8000: 닫힘"
fi

# 연결 테스트
echo "🌐 연결 테스트 중..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost | grep -q "200\|301\|302"; then
    echo "✅ 로컬 연결: 성공"
else
    echo "❌ 로컬 연결: 실패"
fi

echo ""
echo "✅ 배포가 완료되었습니다!"
echo "🌐 웹사이트 확인: http://54.180.71.125"
echo ""
echo "📋 추가 작업 필요:"
echo "1. .env 파일의 실제 값 입력"
echo "2. nginx.conf에서 도메인/IP 수정"
echo "3. SSL 인증서 설치 (Let's Encrypt 권장)"
echo "4. DNS 설정 (도메인 사용 시)"
echo ""
echo "📊 서비스 상태 확인:"
echo "sudo systemctl status django-board"
echo "sudo systemctl status nginx"
