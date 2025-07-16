from django.db import models
from django.utils import timezone


class ChatRoom(models.Model):
    """
    채팅방 모델
    각 채팅방은 독립적인 대화 세션을 나타냅니다.
    """
    title = models.CharField(
        max_length=200, 
        help_text="채팅방 제목 (첫 번째 메시지 기반 자동 생성 또는 사용자 지정)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="채팅방 생성 시간"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="마지막 활동 시간"
    )
    
    class Meta:
        ordering = ['-updated_at']  # 최근 활동 순으로 정렬
        verbose_name = "채팅방"
        verbose_name_plural = "채팅방들"
    
    def __str__(self):
        return f"{self.title} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
    
    def get_message_count(self):
        """채팅방의 총 메시지 수를 반환"""
        return self.messages.count()
    
    def get_last_message(self):
        """채팅방의 마지막 메시지를 반환"""
        return self.messages.order_by('-created_at').first()


class Message(models.Model):
    """
    메시지 모델
    사용자와 AI 간의 개별 메시지를 저장합니다.
    """
    SENDER_CHOICES = [
        ('human', '사용자'),
        ('ai', 'AI'),
    ]
    
    chat_room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text="메시지가 속한 채팅방"
    )
    sender = models.CharField(
        max_length=10,
        choices=SENDER_CHOICES,
        help_text="메시지 발신자 (human 또는 ai)"
    )
    content = models.TextField(
        help_text="메시지 내용"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="메시지 생성 시간"
    )
    
    class Meta:
        ordering = ['created_at']  # 시간 순으로 정렬
        verbose_name = "메시지"
        verbose_name_plural = "메시지들"
    
    def __str__(self):
        content_preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"[{self.get_sender_display()}] {content_preview}"
