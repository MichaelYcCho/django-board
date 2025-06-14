import os
import django
from pathlib import Path

# Django 설정
BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "board_project.settings")
django.setup()

import boto3
from django.conf import settings
from botocore.exceptions import ClientError, NoCredentialsError


def test_s3_connection():
    """S3 연결 테스트"""
    print("🔍 S3 연결 테스트를 시작합니다...")

    # 환경변수 확인
    print(
        f"AWS_ACCESS_KEY_ID: {settings.AWS_ACCESS_KEY_ID[:10]}..."
        if settings.AWS_ACCESS_KEY_ID
        else "None"
    )
    print(
        f"AWS_SECRET_ACCESS_KEY: {'설정됨' if settings.AWS_SECRET_ACCESS_KEY else 'None'}"
    )
    print(f"AWS_STORAGE_BUCKET_NAME: {settings.AWS_STORAGE_BUCKET_NAME}")
    print(f"AWS_S3_REGION_NAME: {settings.AWS_S3_REGION_NAME}")

    try:
        # S3 클라이언트 생성
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        # 버킷 목록 조회 테스트
        print("\n📋 버킷 목록을 조회 중...")
        response = s3_client.list_buckets()
        buckets = [bucket["Name"] for bucket in response["Buckets"]]
        print(f"사용 가능한 버킷: {buckets}")

        # 지정된 버킷 존재 확인
        if settings.AWS_STORAGE_BUCKET_NAME in buckets:
            print(f"✅ 버킷 '{settings.AWS_STORAGE_BUCKET_NAME}'이 존재합니다.")

            # 버킷 내용 확인
            print(f"\n📁 버킷 '{settings.AWS_STORAGE_BUCKET_NAME}' 내용 확인 중...")
            try:
                response = s3_client.list_objects_v2(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix="media/", MaxKeys=10
                )

                if "Contents" in response:
                    print(
                        f"미디어 폴더에 {len(response['Contents'])}개의 파일이 있습니다:"
                    )
                    for obj in response["Contents"][:5]:  # 최대 5개만 표시
                        print(f"  - {obj['Key']}")
                else:
                    print("미디어 폴더가 비어있습니다.")

            except ClientError as e:
                print(f"⚠️ 버킷 내용 조회 중 오류: {e}")

        else:
            print(f"❌ 버킷 '{settings.AWS_STORAGE_BUCKET_NAME}'을 찾을 수 없습니다.")

        print("\n✅ S3 연결 테스트가 완료되었습니다.")
        return True

    except NoCredentialsError:
        print("❌ AWS 자격증명이 설정되지 않았습니다.")
        return False
    except ClientError as e:
        print(f"❌ AWS 클라이언트 오류: {e}")
        return False
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        return False


if __name__ == "__main__":
    test_s3_connection()
