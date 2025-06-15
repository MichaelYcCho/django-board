#!/bin/bash

# 서비스 강제 재시작 스크립트
set -e

echo "🔄 서비스 재시작을 시작합니다..."

# Nginx 설정 다시 복사 및 테스트
echo "🌐 Nginx 설정 업데이트 중..."
sudo cp /home/ubuntu/django-board/nginx.conf /etc/nginx/sites-available/django-board
sudo nginx -t

# Django 서비스 강제 재시작
echo "🔄 Django 서비스 재시작 중..."
sudo systemctl stop django-board
sleep 1
sudo systemctl start django-board

# Nginx 강제 재시작 
echo "🔄 Nginx 재시작 중..."
sudo systemctl stop nginx
sleep 1
sudo systemctl start nginx

# 서비스 상태 확인
echo "📊 서비스 상태 확인 중..."
sleep 3

echo "Django 서비스 상태:"
sudo systemctl status django-board --no-pager -l

echo "Nginx 서비스 상태:"
sudo systemctl status nginx --no-pager -l

# 연결 테스트
echo "🌐 연결 테스트 중..."
for i in {1..5}; do
    if curl -s -o /dev/null -w "%{http_code}" http://localhost | grep -q "200\|301\|302"; then
        echo "✅ 연결 성공 (${i}번째 시도)"
        break
    else
        echo "⏳ 연결 대기 중... (${i}/5)"
        sleep 2
    fi
done

echo ""
echo "✅ 서비스 재시작이 완료되었습니다!"
echo "🌐 웹사이트 확인: http://54.180.71.125"
