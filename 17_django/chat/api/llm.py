from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

class Chatting:
    """
    대화형 AI 채팅 클래스.    
    GPT 모델을 사용하여 사용자와 대화를 수행하고, 대화 기록을 관리한다.
    """

    def __init__(self):
        """LLM 과 대화하는 Chain을 구성한다.
        """
        model = ChatOpenAI(model="gpt-4o-mini")
        prompt_template = ChatPromptTemplate(
            [
                ("system", "너는 나의 친구야. 친근한 말투로 대화를 진행해줘."),
                MessagesPlaceholder(variable_name="history", optional=True),
                ("user", "{query}")
            ]
        )
        output_parser = StrOutputParser()
        self.chain = prompt_template | model | output_parser    

    def send_message(self, message:str, history:list):
        """
        사용자 메시지를 처리하고 AI 응답을 반환.
        Parameter:
            message: str 사용자가 입력한 메시지
            history: list - 사용자와 AI간의 이전까지의 대화 기록

        Returns:
            str: AI의 응답 메시지
        """
        response = self.chain.invoke({"history": history, "query": message})
        
        return response
    


def add_message_to_history(history:list[tuple[str, str]], message:tuple[str, str], max_history=20):
    """
    Message를 history에 추가하는 util 메소드.
    파라미터로 받은 history에 message를 추가한다.
    max_history 개수를 넘어가면 오래된 것 부터 지운다.
    Parameter:
        history: list - 대화 기록
        message: tuple - (speaker, message) 형태의 메시지
        max_history: int - 저장할 최대 대화 기록 개수
    """
    while len(history) >= max_history:
        history.pop(0)
    history.append(message)


def get_chat_history(chat_room_id: int, max_messages: int = 20) -> list[tuple[str, str]]:
    """
    데이터베이스에서 채팅방의 대화 히스토리를 가져오는 함수.

    Parameter:
        chat_room_id: int - 채팅방 ID
        max_messages: int - 가져올 최대 메시지 수 (기본값: 20)

    Returns:
        list[tuple[str, str]] - (sender, content) 형태의 메시지 리스트
    """
    from .models import Message

    # 최근 메시지부터 max_messages 개수만큼 가져오기
    messages = Message.objects.filter(
        chat_room_id=chat_room_id
    ).order_by('-created_at')[:max_messages]

    # 시간 순으로 정렬하여 반환 (오래된 것부터)
    history = []
    for message in reversed(messages):
        history.append((message.sender, message.content))

    return history