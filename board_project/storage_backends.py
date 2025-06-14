from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """미디어 파일용 S3 스토리지"""

    location = "media"
    file_overwrite = False
    # ACL 비활성화된 버킷에서는 default_acl 제거

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class StaticStorage(S3Boto3Storage):
    """정적 파일용 S3 스토리지"""

    location = "static"
    # ACL 비활성화된 버킷에서는 default_acl 제거
