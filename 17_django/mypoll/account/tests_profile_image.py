# account/tests_profile_image.py
import os
import tempfile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

User = get_user_model()

class ProfileImageTestCase(TestCase):
    def setUp(self):
        """테스트 설정"""
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'password1': 'testpass123!',
            'password2': 'testpass123!',
            'name': '테스트사용자',
            'email': 'test@example.com',
            'birthday': '1990-01-01'
        }
        
    def create_test_image(self, name='test.jpg', size=(100, 100), color='RGB'):
        """테스트용 이미지 파일 생성"""
        file = io.BytesIO()
        image = Image.new(color, size)
        image.save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile(name, file.getvalue(), content_type='image/jpeg')
    
    def test_user_creation_with_profile_image(self):
        """프로필 이미지와 함께 회원가입 테스트"""
        # 테스트 이미지 생성
        test_image = self.create_test_image('profile.jpg')
        
        # 회원가입 데이터에 프로필 이미지 추가
        signup_data = self.user_data.copy()
        signup_data['profile_image'] = test_image
        
        # 회원가입 요청
        response = self.client.post(reverse('account:create'), signup_data)
        
        # 회원가입 성공 확인 (홈페이지로 리다이렉트)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        
        # 사용자가 생성되었는지 확인
        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user.profile_image)
        self.assertTrue(user.profile_image.name.startswith('images/'))
        
    def test_user_creation_without_profile_image(self):
        """프로필 이미지 없이 회원가입 테스트"""
        response = self.client.post(reverse('account:create'), self.user_data)
        
        # 회원가입 성공 확인
        self.assertEqual(response.status_code, 302)
        
        # 사용자가 생성되었는지 확인
        user = User.objects.get(username='testuser')
        self.assertFalse(user.profile_image)  # 프로필 이미지가 없어야 함
        
    def test_profile_image_display_in_detail_page(self):
        """회원정보 페이지에서 프로필 이미지 표시 테스트"""
        # 프로필 이미지와 함께 사용자 생성
        test_image = self.create_test_image('profile.jpg')
        user = User.objects.create_user(
            username='testuser',
            password='testpass123!',
            name='테스트사용자',
            email='test@example.com',
            profile_image=test_image
        )
        
        # 로그인
        self.client.login(username='testuser', password='testpass123!')
        
        # 회원정보 페이지 접근
        response = self.client.get(reverse('account:detail'))
        self.assertEqual(response.status_code, 200)
        
        # 프로필 이미지가 템플릿에 포함되어 있는지 확인
        self.assertContains(response, '/media/images/')
        self.assertContains(response, 'img-thumbnail')
        
    def test_profile_image_update(self):
        """프로필 이미지 수정 테스트"""
        # 사용자 생성
        user = User.objects.create_user(
            username='testuser',
            password='testpass123!',
            name='테스트사용자',
            email='test@example.com'
        )
        
        # 로그인
        self.client.login(username='testuser', password='testpass123!')
        
        # 새 프로필 이미지 생성
        new_image = self.create_test_image('new_profile.jpg')
        
        # 회원정보 수정 요청
        update_data = {
            'name': '수정된이름',
            'email': 'updated@example.com',
            'birthday': '1995-05-05',
            'profile_image': new_image
        }
        
        response = self.client.post(reverse('account:update'), update_data)
        
        # 수정 성공 확인
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account:detail'))
        
        # 사용자 정보가 업데이트되었는지 확인
        user.refresh_from_db()
        self.assertEqual(user.name, '수정된이름')
        self.assertIsNotNone(user.profile_image)
        
    def test_invalid_image_file(self):
        """잘못된 이미지 파일 업로드 테스트"""
        # 텍스트 파일을 이미지로 위장
        fake_image = SimpleUploadedFile(
            "fake.jpg", 
            b"This is not an image", 
            content_type="image/jpeg"
        )
        
        signup_data = self.user_data.copy()
        signup_data['profile_image'] = fake_image
        
        response = self.client.post(reverse('account:create'), signup_data)
        
        # 폼 에러가 발생해야 함
        self.assertEqual(response.status_code, 200)  # 다시 폼 페이지로
        self.assertContains(response, 'form')  # 폼이 다시 표시되어야 함
        
    def test_large_image_file(self):
        """큰 이미지 파일 업로드 테스트"""
        # 큰 이미지 생성 (1000x1000)
        large_image = self.create_test_image('large.jpg', size=(1000, 1000))
        
        signup_data = self.user_data.copy()
        signup_data['profile_image'] = large_image
        
        response = self.client.post(reverse('account:create'), signup_data)
        
        # 업로드가 성공해야 함 (Django는 기본적으로 파일 크기 제한이 없음)
        self.assertEqual(response.status_code, 302)
        
        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user.profile_image)
        
    def tearDown(self):
        """테스트 후 정리"""
        # 테스트 중 생성된 미디어 파일들 정리
        for user in User.objects.all():
            if user.profile_image:
                if os.path.exists(user.profile_image.path):
                    os.remove(user.profile_image.path)
