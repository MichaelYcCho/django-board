# EC2 배포 가이드 (SQLite3 버전)

## 1. EC2 인스턴스 준비

### EC2 인스턴스 생성
- **AMI**: Ubuntu 22.04 LTS
- **인스턴스 타입**: t3.micro 이상 (단기 프로젝트용)
- **스토리지**: 10GB 이상
- **보안 그룹**: HTTP(80), HTTPS(443), SSH(22) 포트 열기

### SSH 접속
```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

## 2. 프로젝트 배포

### GitHub에 프로젝트 업로드
```bash
# 로컬에서 실행
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/django-board.git
git push -u origin main
```

### 배포 스크립트 실행
```bash
# EC2에서 실행
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/django-board/main/deploy.sh
chmod +x deploy.sh
./deploy.sh
```

## 3. 수동 설정

### 환경변수 설정
```bash
cd /var/www/django-board
sudo nano .env
```

`.env` 파일 내용:
```
DEBUG=False
SECRET_KEY=your-super-secret-key-here-at-least-50-characters-long
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=estedu-img
AWS_S3_REGION_NAME=ap-northeast-2
AWS_S3_CUSTOM_DOMAIN=s3_url
```

### Nginx 설정 수정
```bash
sudo nano /etc/nginx/sites-available/django-board
```

`server_name`을 실제 도메인 또는 IP로 변경:
```nginx
server_name your-domain.com your-ec2-public-ip;
```

### 서비스 재시작
```bash
sudo systemctl restart django-board
sudo systemctl restart nginx
```

## 4. SSL 인증서 설치 (선택사항)

### Let's Encrypt 설치
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### SSL 설정 활성화
```bash
cd /var/www/django-board
sudo nano board_project/settings_prod.py
```

다음 설정을 `True`로 변경:
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 5. 모니터링 및 유지보수

### 로그 확인
```bash
# Django 로그
sudo tail -f /var/log/django/django-board.log

# Gunicorn 로그
sudo tail -f /var/log/gunicorn/error.log

# Nginx 로그
sudo tail -f /var/log/nginx/error.log
```

### 서비스 상태 확인
```bash
sudo systemctl status django-board
sudo systemctl status nginx
```

### 프로젝트 업데이트
```bash
cd /var/www/django-board
git pull origin main
source venv/bin/activate
pip install -r requirements-prod.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart django-board
```

### SQLite3 데이터베이스 백업
```bash
# 데이터베이스 백업
cp /var/www/django-board/db.sqlite3 /var/www/django-board/db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)

# 정기 백업 크론잡 설정
crontab -e
# 매일 새벽 2시에 백업
0 2 * * * cp /var/www/django-board/db.sqlite3 /var/www/django-board/db.sqlite3.backup.$(date +\%Y\%m\%d)
```

## 6. 보안 강화

### 자동 보안 업데이트
```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### Fail2Ban 설치
```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 정기 백업 설정
```bash
# SQLite3 데이터베이스 백업 스크립트 생성
sudo nano /usr/local/bin/db-backup.sh

#!/bin/bash
BACKUP_DIR="/var/backups/django-board"
sudo mkdir -p $BACKUP_DIR
cp /var/www/django-board/db.sqlite3 $BACKUP_DIR/db.sqlite3.$(date +%Y%m%d_%H%M%S)
# 7일 이상 된 백업 파일 삭제
find $BACKUP_DIR -name "*.sqlite3.*" -mtime +7 -delete

# 실행 권한 부여
sudo chmod +x /usr/local/bin/db-backup.sh

# 크론탭에 등록 (매일 새벽 2시)
echo "0 2 * * * /usr/local/bin/db-backup.sh" | sudo crontab -
```

## 7. 성능 최적화

### Redis 설치 (캐싱용)
```bash
sudo apt install redis-server
```

### 정적 파일 압축
- WhiteNoise가 자동으로 처리

### 데이터베이스 최적화
- SQLite3 VACUUM 명령으로 데이터베이스 최적화
- 인덱스 최적화

## 트러블슈팅

### 일반적인 문제들

1. **502 Bad Gateway**
   - Gunicorn 서비스 상태 확인
   - 로그 파일 확인

2. **정적 파일 404**
   - `collectstatic` 재실행
   - Nginx 설정 확인

3. **데이터베이스 연결 오류**
   - SQLite3 파일 권한 확인
   - 환경변수 설정 확인

4. **S3 업로드 실패**
   - AWS 자격증명 확인
   - 버킷 권한 설정 확인
