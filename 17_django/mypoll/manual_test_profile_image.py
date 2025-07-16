#!/usr/bin/env python
"""
프로필 이미지 기능 수동 테스트 스크립트
Django 서버가 실행 중일 때 이 스크립트를 실행하여 프로필 이미지 기능을 테스트할 수 있습니다.
"""

import os
import sys
import django
from django.conf import settings

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

User = get_user_model()

def create_test_image(name='test.jpg', size=(100, 100), color='RGB'):
    """테스트용 이미지 파일 생성"""
    file = io.BytesIO()
    image = Image.new(color, size)
    image.save(file, 'JPEG')
    file.seek(0)
    return SimpleUploadedFile(name, file.getvalue(), content_type='image/jpeg')

def test_profile_image_functionality():
    """프로필 이미지 기능 테스트"""
    print("=== 프로필 이미지 기능 테스트 시작 ===\n")
    
    # 1. 기존 테스트 사용자 삭제 (있다면)
    try:
        existing_user = User.objects.get(username='test_profile_user')
        if existing_user.profile_image:
            # 기존 프로필 이미지 파일 삭제
            if os.path.exists(existing_user.profile_image.path):
                os.remove(existing_user.profile_image.path)
                print("기존 프로필 이미지 파일 삭제됨")
        existing_user.delete()
        print("기존 테스트 사용자 삭제됨")
    except User.DoesNotExist:
        print("기존 테스트 사용자 없음")
    
    # 2. 프로필 이미지와 함께 사용자 생성
    print("\n1. 프로필 이미지와 함께 사용자 생성 테스트")
    test_image = create_test_image('profile_test.jpg', size=(200, 200))
    
    user = User.objects.create_user(
        username='test_profile_user',
        password='testpass123!',
        name='프로필테스트사용자',
        email='profile_test@example.com',
        profile_image=test_image
    )
    
    print(f"✓ 사용자 생성됨: {user.username}")
    print(f"✓ 프로필 이미지 경로: {user.profile_image.name}")
    print(f"✓ 프로필 이미지 URL: {user.profile_image.url}")
    
    # 파일이 실제로 저장되었는지 확인
    if os.path.exists(user.profile_image.path):
        print(f"✓ 프로필 이미지 파일이 실제로 저장됨: {user.profile_image.path}")
        file_size = os.path.getsize(user.profile_image.path)
        print(f"✓ 파일 크기: {file_size} bytes")
    else:
        print("✗ 프로필 이미지 파일이 저장되지 않음")
    
    # 3. 프로필 이미지 업데이트 테스트
    print("\n2. 프로필 이미지 업데이트 테스트")
    old_image_path = user.profile_image.path
    
    new_test_image = create_test_image('new_profile_test.jpg', size=(150, 150))
    user.profile_image = new_test_image
    user.save()
    
    print(f"✓ 프로필 이미지 업데이트됨")
    print(f"✓ 새 프로필 이미지 경로: {user.profile_image.name}")
    print(f"✓ 새 프로필 이미지 URL: {user.profile_image.url}")
    
    # 새 파일이 저장되었는지 확인
    if os.path.exists(user.profile_image.path):
        print(f"✓ 새 프로필 이미지 파일이 저장됨: {user.profile_image.path}")
        file_size = os.path.getsize(user.profile_image.path)
        print(f"✓ 파일 크기: {file_size} bytes")
    else:
        print("✗ 새 프로필 이미지 파일이 저장되지 않음")
    
    # 4. 프로필 이미지 없는 사용자 테스트
    print("\n3. 프로필 이미지 없는 사용자 테스트")
    user_no_image = User.objects.create_user(
        username='test_no_image_user',
        password='testpass123!',
        name='이미지없는사용자',
        email='no_image@example.com'
    )
    
    print(f"✓ 프로필 이미지 없는 사용자 생성됨: {user_no_image.username}")
    print(f"✓ 프로필 이미지 필드 값: {user_no_image.profile_image}")
    print(f"✓ 프로필 이미지 존재 여부: {bool(user_no_image.profile_image)}")
    
    # 5. 웹 접근 테스트 안내
    print("\n4. 웹 브라우저 테스트 안내")
    print("다음 URL들을 브라우저에서 테스트해보세요:")
    print("- 회원가입: http://127.0.0.1:8000/account/create")
    print("- 로그인: http://127.0.0.1:8000/account/login")
    print("  (테스트 계정: test_profile_user / testpass123!)")
    print("- 회원정보 조회: http://127.0.0.1:8000/account/detail")
    print("- 회원정보 수정: http://127.0.0.1:8000/account/update")
    
    print("\n=== 테스트 완료 ===")
    print("브라우저에서 위 URL들을 테스트하여 프로필 이미지 기능이 정상 작동하는지 확인하세요.")
    
    # 정리
    print("\n5. 정리 작업")
    try:
        # 테스트 사용자들 삭제
        for username in ['test_profile_user', 'test_no_image_user']:
            try:
                test_user = User.objects.get(username=username)
                if test_user.profile_image and os.path.exists(test_user.profile_image.path):
                    os.remove(test_user.profile_image.path)
                    print(f"✓ {username}의 프로필 이미지 파일 삭제됨")
                test_user.delete()
                print(f"✓ {username} 사용자 삭제됨")
            except User.DoesNotExist:
                pass
    except Exception as e:
        print(f"정리 작업 중 오류: {e}")

if __name__ == "__main__":
    test_profile_image_functionality()
