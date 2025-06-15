# Gunicorn 설정 파일
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
reload = False

# 로깅
# accesslog = "/var/log/gunicorn/access.log"
# errorlog = "/var/log/gunicorn/error.log"
# loglevel = "info"

# 프로세스 관리
# user = "ubuntu"
# group = "ubuntu"
# tmp_upload_dir = None

# 보안
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# gunicorn --bind 0.0.0.0:8000 board_project.wsgi:application
