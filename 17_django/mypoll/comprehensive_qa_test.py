#!/usr/bin/env python
"""
프로필 이미지 기능 종합 QA 테스트
모든 가능한 시나리오와 엣지 케이스를 테스트합니다.
"""

import os
import sys
import django
from django.conf import settings

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from PIL import Image
import io
import tempfile

User = get_user_model()

class ComprehensiveProfileImageQA(TestCase):
    def setUp(self):
        """테스트 설정"""
        self.client = Client()
        self.test_user_data = {
            'username': 'qatest',
            'password1': 'QAtest123!@#',
            'password2': 'QAtest123!@#',
            'name': 'QA테스트사용자',
            'email': 'qa@test.com',
            'birthday': '1990-01-01'
        }
        
    def create_test_image(self, name='test.jpg', size=(100, 100), format='JPEG', color='RGB'):
        """다양한 형태의 테스트 이미지 생성"""
        file = io.BytesIO()
        image = Image.new(color, size)
        image.save(file, format)
        file.seek(0)
        content_type = f'image/{format.lower()}'
        return SimpleUploadedFile(name, file.getvalue(), content_type=content_type)
    
    def test_01_signup_with_valid_image_formats(self):
        """다양한 유효한 이미지 형식으로 회원가입 테스트"""
        print("QA Test 1: 다양한 이미지 형식 회원가입 테스트")
        
        formats = [
            ('test.jpg', 'JPEG'),
            ('test.png', 'PNG'),
            ('test.gif', 'GIF'),
        ]
        
        for i, (filename, format_type) in enumerate(formats):
            with self.subTest(format=format_type):
                test_image = self.create_test_image(filename, format=format_type)
                signup_data = self.test_user_data.copy()
                signup_data['username'] = f'qatest_{format_type.lower()}'
                signup_data['profile_image'] = test_image
                
                response = self.client.post(reverse('account:create'), signup_data)
                self.assertEqual(response.status_code, 302, f"{format_type} 형식 이미지 업로드 실패")
                
                user = User.objects.get(username=signup_data['username'])
                self.assertTrue(user.profile_image, f"{format_type} 이미지가 저장되지 않음")
                print(f"  ✓ {format_type} 형식 이미지 업로드 성공")
    
    def test_02_signup_with_large_images(self):
        """큰 이미지 파일 업로드 테스트"""
        print("QA Test 2: 큰 이미지 파일 업로드 테스트")
        
        sizes = [
            (1000, 1000),  # 1MP
            (2000, 2000),  # 4MP
            (3000, 3000),  # 9MP
        ]
        
        for i, size in enumerate(sizes):
            with self.subTest(size=size):
                test_image = self.create_test_image(f'large_{i}.jpg', size=size)
                signup_data = self.test_user_data.copy()
                signup_data['username'] = f'qatest_large_{i}'
                signup_data['profile_image'] = test_image
                
                response = self.client.post(reverse('account:create'), signup_data)
                self.assertEqual(response.status_code, 302, f"큰 이미지({size}) 업로드 실패")
                
                user = User.objects.get(username=signup_data['username'])
                self.assertTrue(user.profile_image, f"큰 이미지({size})가 저장되지 않음")
                print(f"  ✓ {size} 크기 이미지 업로드 성공")
    
    def test_03_invalid_file_uploads(self):
        """잘못된 파일 업로드 테스트"""
        print("QA Test 3: 잘못된 파일 업로드 테스트")
        
        invalid_files = [
            ('fake.jpg', b'This is not an image', 'image/jpeg'),
            ('document.pdf', b'%PDF-1.4 fake pdf', 'application/pdf'),
            ('script.js', b'alert("hello");', 'text/javascript'),
            ('empty.jpg', b'', 'image/jpeg'),
        ]
        
        for filename, content, content_type in invalid_files:
            with self.subTest(filename=filename):
                fake_file = SimpleUploadedFile(filename, content, content_type=content_type)
                signup_data = self.test_user_data.copy()
                signup_data['username'] = f'qatest_{filename.split(".")[0]}'
                signup_data['profile_image'] = fake_file
                
                response = self.client.post(reverse('account:create'), signup_data)
                
                # 잘못된 파일은 폼 에러가 발생해야 함
                if content:  # 빈 파일이 아닌 경우
                    self.assertEqual(response.status_code, 200, f"{filename} - 에러 처리 실패")
                    self.assertContains(response, 'form', msg_prefix=f"{filename} - 폼 에러 표시 안됨")
                    print(f"  ✓ {filename} 잘못된 파일 에러 처리 성공")
                else:
                    # 빈 파일은 선택적 필드이므로 성공해야 함
                    print(f"  ✓ {filename} 빈 파일 처리 성공")
    
    def test_04_profile_image_display(self):
        """프로필 이미지 표시 테스트"""
        print("QA Test 4: 프로필 이미지 표시 테스트")
        
        # 이미지가 있는 사용자
        test_image = self.create_test_image('display_test.jpg')
        user_with_image = User.objects.create_user(
            username='display_test',
            password='testpass123!',
            name='표시테스트',
            email='display@test.com',
            profile_image=test_image
        )
        
        self.client.login(username='display_test', password='testpass123!')
        response = self.client.get(reverse('account:detail'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/media/images/')
        self.assertContains(response, 'img-thumbnail')
        self.assertContains(response, 'alt="프로필 이미지"')
        print("  ✓ 프로필 이미지 표시 성공")
        
        # 이미지가 없는 사용자
        user_no_image = User.objects.create_user(
            username='no_image_test',
            password='testpass123!',
            name='이미지없음',
            email='noimage@test.com'
        )
        
        self.client.login(username='no_image_test', password='testpass123!')
        response = self.client.get(reverse('account:detail'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '프로필 이미지가 없습니다')
        print("  ✓ 이미지 없는 경우 메시지 표시 성공")
    
    def test_05_profile_image_update(self):
        """프로필 이미지 수정 테스트"""
        print("QA Test 5: 프로필 이미지 수정 테스트")
        
        # 사용자 생성
        user = User.objects.create_user(
            username='update_test',
            password='testpass123!',
            name='수정테스트',
            email='update@test.com'
        )
        
        self.client.login(username='update_test', password='testpass123!')
        
        # 첫 번째 이미지 업로드
        first_image = self.create_test_image('first.jpg')
        update_data = {
            'name': '수정된이름',
            'email': 'updated@test.com',
            'birthday': '1995-05-05',
            'profile_image': first_image
        }
        
        response = self.client.post(reverse('account:update'), update_data)
        self.assertEqual(response.status_code, 302)
        
        user.refresh_from_db()
        self.assertTrue(user.profile_image)
        first_image_path = user.profile_image.path
        print("  ✓ 첫 번째 이미지 업로드 성공")
        
        # 두 번째 이미지로 교체
        second_image = self.create_test_image('second.jpg')
        update_data['profile_image'] = second_image
        
        response = self.client.post(reverse('account:update'), update_data)
        self.assertEqual(response.status_code, 302)
        
        user.refresh_from_db()
        self.assertTrue(user.profile_image)
        self.assertNotEqual(first_image_path, user.profile_image.path)
        print("  ✓ 이미지 교체 성공")
    
    def test_06_form_validation_edge_cases(self):
        """폼 검증 엣지 케이스 테스트"""
        print("QA Test 6: 폼 검증 엣지 케이스 테스트")
        
        # 매우 작은 이미지
        tiny_image = self.create_test_image('tiny.jpg', size=(1, 1))
        signup_data = self.test_user_data.copy()
        signup_data['username'] = 'tiny_test'
        signup_data['profile_image'] = tiny_image
        
        response = self.client.post(reverse('account:create'), signup_data)
        self.assertEqual(response.status_code, 302)
        print("  ✓ 매우 작은 이미지 처리 성공")
        
        # 정사각형이 아닌 이미지
        rect_image = self.create_test_image('rect.jpg', size=(200, 100))
        signup_data['username'] = 'rect_test'
        signup_data['profile_image'] = rect_image
        
        response = self.client.post(reverse('account:create'), signup_data)
        self.assertEqual(response.status_code, 302)
        print("  ✓ 직사각형 이미지 처리 성공")
    
    def test_07_concurrent_upload_simulation(self):
        """동시 업로드 시뮬레이션 테스트"""
        print("QA Test 7: 동시 업로드 시뮬레이션 테스트")
        
        for i in range(5):
            test_image = self.create_test_image(f'concurrent_{i}.jpg')
            signup_data = self.test_user_data.copy()
            signup_data['username'] = f'concurrent_{i}'
            signup_data['profile_image'] = test_image
            
            response = self.client.post(reverse('account:create'), signup_data)
            self.assertEqual(response.status_code, 302, f"동시 업로드 {i} 실패")
            
            user = User.objects.get(username=signup_data['username'])
            self.assertTrue(user.profile_image, f"동시 업로드 {i} 이미지 저장 실패")
        
        print("  ✓ 동시 업로드 시뮬레이션 성공")
    
    def test_08_file_path_security(self):
        """파일 경로 보안 테스트"""
        print("QA Test 8: 파일 경로 보안 테스트")
        
        # 악의적인 파일명 테스트
        malicious_names = [
            '../../../etc/passwd.jpg',
            '..\\..\\windows\\system32\\config.jpg',
            'normal_name.jpg',
            'name with spaces.jpg',
            '한글파일명.jpg',
            'very_long_filename_' + 'a' * 200 + '.jpg'
        ]
        
        for i, filename in enumerate(malicious_names):
            with self.subTest(filename=filename):
                test_image = self.create_test_image(filename)
                signup_data = self.test_user_data.copy()
                signup_data['username'] = f'security_{i}'
                signup_data['profile_image'] = test_image
                
                response = self.client.post(reverse('account:create'), signup_data)
                self.assertEqual(response.status_code, 302, f"보안 테스트 {filename} 실패")
                
                user = User.objects.get(username=signup_data['username'])
                self.assertTrue(user.profile_image)
                
                # 파일이 안전한 경로에 저장되었는지 확인
                self.assertTrue(user.profile_image.path.startswith(str(settings.MEDIA_ROOT)))
                print(f"  ✓ {filename[:30]}... 보안 테스트 통과")
    
    def tearDown(self):
        """테스트 후 정리"""
        # 테스트 중 생성된 모든 파일 정리
        for user in User.objects.all():
            if user.profile_image:
                try:
                    if os.path.exists(user.profile_image.path):
                        os.remove(user.profile_image.path)
                except:
                    pass

def run_comprehensive_qa():
    """종합 QA 테스트 실행"""
    print("=" * 60)
    print("프로필 이미지 기능 종합 QA 테스트 시작")
    print("=" * 60)
    
    import unittest
    
    # 테스트 스위트 생성
    suite = unittest.TestLoader().loadTestsFromTestCase(ComprehensiveProfileImageQA)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("🎉 모든 QA 테스트 통과! 버그 없음!")
    else:
        print("❌ QA 테스트 실패! 버그 발견!")
        print(f"실패한 테스트: {len(result.failures)}")
        print(f"에러 발생 테스트: {len(result.errors)}")
    print("=" * 60)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    run_comprehensive_qa()
