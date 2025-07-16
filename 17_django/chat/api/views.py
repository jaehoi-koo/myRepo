from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
import json
from datetime import datetime

from .models import ChatRoom, Message
from .llm import Chatting, get_chat_history


@method_decorator(csrf_exempt, name='dispatch')
class ChatRoomListView(View):
    """채팅방 목록 조회 및 생성"""

    def get(self, request):
        """채팅방 목록 반환"""
        chatrooms = ChatRoom.objects.all()
        data = []
        for room in chatrooms:
            last_message = room.get_last_message()
            data.append({
                'id': room.id,
                'title': room.title,
                'created_at': room.created_at.isoformat(),
                'updated_at': room.updated_at.isoformat(),
                'message_count': room.get_message_count(),
                'last_message': {
                    'content': last_message.content[:50] + '...' if last_message and len(last_message.content) > 50 else last_message.content if last_message else None,
                    'sender': last_message.sender if last_message else None,
                    'created_at': last_message.created_at.isoformat() if last_message else None
                } if last_message else None
            })
        return JsonResponse({'chatrooms': data})

    @method_decorator(csrf_exempt)
    def post(self, request):
        """새 채팅방 생성"""
        try:
            data = json.loads(request.body.decode('utf-8')) if request.body else {}
            title = data.get('title', f"새 채팅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")

            chatroom = ChatRoom.objects.create(title=title)

            return JsonResponse({
                'id': chatroom.id,
                'title': chatroom.title,
                'created_at': chatroom.created_at.isoformat(),
                'updated_at': chatroom.updated_at.isoformat(),
                'message_count': 0
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ChatRoomDetailView(View):
    """특정 채팅방 조회, 수정, 삭제"""

    def get(self, request, room_id):
        """채팅방 정보 반환"""
        chatroom = get_object_or_404(ChatRoom, id=room_id)
        return JsonResponse({
            'id': chatroom.id,
            'title': chatroom.title,
            'created_at': chatroom.created_at.isoformat(),
            'updated_at': chatroom.updated_at.isoformat(),
            'message_count': chatroom.get_message_count()
        })

    @method_decorator(csrf_exempt)
    def put(self, request, room_id):
        """채팅방 제목 수정"""
        try:
            chatroom = get_object_or_404(ChatRoom, id=room_id)
            data = json.loads(request.body.decode('utf-8'))

            if 'title' in data:
                chatroom.title = data['title']
                chatroom.save()

            return JsonResponse({
                'id': chatroom.id,
                'title': chatroom.title,
                'updated_at': chatroom.updated_at.isoformat()
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    @method_decorator(csrf_exempt)
    def delete(self, request, room_id):
        """채팅방 삭제"""
        try:
            chatroom = get_object_or_404(ChatRoom, id=room_id)
            chatroom.delete()
            return JsonResponse({'message': '채팅방이 삭제되었습니다.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class MessageListView(View):
    """채팅방의 메시지 목록 조회 및 새 메시지 전송"""

    def get(self, request, room_id):
        """채팅방의 메시지 목록 반환"""
        chatroom = get_object_or_404(ChatRoom, id=room_id)
        messages = chatroom.messages.all()

        data = []
        for message in messages:
            data.append({
                'id': message.id,
                'sender': message.sender,
                'content': message.content,
                'created_at': message.created_at.isoformat()
            })

        return JsonResponse({
            'chatroom_id': chatroom.id,
            'chatroom_title': chatroom.title,
            'messages': data
        })

    @method_decorator(csrf_exempt)
    def post(self, request, room_id):
        """새 메시지 전송 및 AI 응답 생성"""
        try:
            chatroom = get_object_or_404(ChatRoom, id=room_id)
            # 안전한 인코딩 처리
            try:
                body_str = request.body.decode('utf-8')
            except UnicodeDecodeError:
                # 다른 인코딩으로 시도
                body_str = request.body.decode('latin-1')

            data = json.loads(body_str)
            user_message = data.get('message', '').strip()

            if not user_message:
                return JsonResponse({'error': '메시지를 입력해주세요.'}, status=400)

            # 사용자 메시지 저장
            user_msg = Message.objects.create(
                chat_room=chatroom,
                sender='human',
                content=user_message
            )

            # 대화 히스토리 가져오기
            history = get_chat_history(room_id)

            # AI 응답 생성
            chat = Chatting()
            ai_response = chat.send_message(user_message, history)

            # AI 응답 저장
            ai_msg = Message.objects.create(
                chat_room=chatroom,
                sender='ai',
                content=ai_response
            )

            # 채팅방 제목이 기본값이면 첫 번째 메시지로 업데이트
            if chatroom.title.startswith("새 채팅") and chatroom.get_message_count() == 2:
                # 첫 번째 사용자 메시지를 기반으로 제목 생성
                title_preview = user_message[:30] + "..." if len(user_message) > 30 else user_message
                chatroom.title = title_preview
                chatroom.save()

            return JsonResponse({
                'user_message': {
                    'id': user_msg.id,
                    'sender': user_msg.sender,
                    'content': user_msg.content,
                    'created_at': user_msg.created_at.isoformat()
                },
                'ai_message': {
                    'id': ai_msg.id,
                    'sender': ai_msg.sender,
                    'content': ai_msg.content,
                    'created_at': ai_msg.created_at.isoformat()
                },
                'chatroom_title': chatroom.title
            })

        except Exception as e:
            import traceback
            error_details = {
                'error': str(e),
                'traceback': traceback.format_exc()
            }
            return JsonResponse(error_details, status=500)


# 기존 API와의 호환성을 위한 레거시 뷰 (추후 제거 예정)
@require_GET
def chat_message(request, message):
    """
    레거시 API - 기존 프론트엔드와의 호환성을 위해 유지
    추후 새로운 API로 마이그레이션 후 제거 예정
    """
    try:
        # 현재 세션의 채팅방 ID 가져오기 (없으면 새로 생성)
        current_room_id = request.session.get('current_chat_room_id')

        if not current_room_id:
            # 새 채팅방 생성
            chatroom = ChatRoom.objects.create(
                title=f"새 채팅 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )
            request.session['current_chat_room_id'] = chatroom.id
            current_room_id = chatroom.id
        else:
            chatroom = get_object_or_404(ChatRoom, id=current_room_id)

        # 사용자 메시지 저장
        user_msg = Message.objects.create(
            chat_room=chatroom,
            sender='human',
            content=message
        )

        # 대화 히스토리 가져오기
        history = get_chat_history(current_room_id)

        # AI 응답 생성
        chat = Chatting()
        ai_response = chat.send_message(message, history)

        # AI 응답 저장
        ai_msg = Message.objects.create(
            chat_room=chatroom,
            sender='ai',
            content=ai_response
        )

        # 채팅방 제목이 기본값이면 첫 번째 메시지로 업데이트
        if chatroom.title.startswith("새 채팅") and chatroom.get_message_count() == 2:
            title_preview = message[:30] + "..." if len(message) > 30 else message
            chatroom.title = title_preview
            chatroom.save()

        return JsonResponse({'response': ai_response})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
