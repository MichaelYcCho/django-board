"""
Production settings for Django board project
"""

from .settings import *
import os

# 보안 설정
DEBUG = False
ALLOWED_HOSTS = [
    "54.180.71.125",  # EC2 퍼블릭 IP
    "localhost",
    "127.0.0.1",
]

# HTTPS 설정 (Let's Encrypt 등 SSL 인증서 설치 후)
SECURE_SSL_REDIRECT = False  # SSL 인증서 설치 후 True로 변경
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = False  # SSL 인증서 설치 후 True로 변경
CSRF_COOKIE_SECURE = False  # SSL 인증서 설치 후 True로 변경

# 데이터베이스 설정 (SQLite3 - 단기 프로젝트용)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# 정적 파일 설정
STATIC_ROOT = "/home/ubuntu/django-board/staticfiles/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# 로깅 설정
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "/home/ubuntu/django-board/logs/django-board.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
