import os
from typing import Any
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
import openai
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import ThreadPool
import sys

sys.path.append('d:/Progs/PycharmProjects/English/English')
from api.models import Message
from .tasks import get_response


pool = ThreadPool()
executor = ThreadPoolExecutor()


try:
    ChatGTPUser = get_user_model().objects.create(
        username='chat-gpt',
        password='chat-gpt-password',
        location='New York',
        level='C2',
        email='chat_gpt@mail.ru'
    )

except IntegrityError:  # instance exists, it`s OK
    ChatGTPUser = get_user_model().objects.get(username='chat-gpt')


openai_key = os.environ.get('OPENAI_KEY')
if openai_key is None:
    raise ValueError("OpenAI key expected.")
try:
    ...
except openai.error.AuthenticationError:
    raise ValueError("OpenAI key exists, but not valid. Check your key")
openai.api_key = openai_key


class MessengerBase(ABC):
    __slots__ = ()

    def __init__(self):
        pass

    @staticmethod
    def __test_chat() -> None:
        message = "It`s just a test, you may answer with a single dot like `.`"
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message}]
        )
        # may write some logic further
        ...

    @staticmethod
    @abstractmethod
    def get_response(text: Any) -> Any:
        pass


class ChatGPT(MessengerBase):
    __slots__ = ()

    @staticmethod
    def get_response(text: str) -> str:
        return get_response(text)


class Messenger(ChatGPT):
    __slots__ = ('message', 'func')
    user = ChatGTPUser

    def __init__(self, message: Message):
        super().__init__()
        self.message = message
        self.func = lambda mes: (openai.Completion.create(
            model='text-davinci-003',
            temperature=0.5,
            n=1,
            max_tokens=1,
            prompt=mes.text,
        ), mes)

    def chat(self):
        match self.message.type:
            case "remark":
                request_text = self.__reply_to_remark()
            case "pupil":
                request_text = self.__reply_to_pupil()
            case _:
                raise ValueError("Incorrect type")
        response_text = self.get_response(request_text)
        return self.save_answer(response_text)

    def __reply_to_remark(self) -> str:
        text = \
        f"""
            Помоги мне усовершенствовать свой уровень английского языка. Я напишу тебе далее сообщение, 
            а ты должен исправить в нем ошибки и объяснить, в чём я ошибся. Если я всё сделал правильно, то не исправляй.
            Вот мой текст: {self.message.text}
        """
        return text.strip()

    def __reply_to_pupil(self) -> str:
        original_message = self.message.reply_to
        text = \
        f"""
            Помоги мне усовершенствовать свой уровень английского языка. 
            Я должен был перевести на английский язык этот текст: {original_message.text}.
            Я напишу тебе далее свой перевод на английский, а ты должен исправить в нем ошибки и объяснить, в чём я ошибся. 
            Если я всё сделал правильно, то не исправляй.
            Вот мой перевод: {self.message.text}
        """
        return text.strip()

    def save_answer(self, text: str) -> None:
        answer_message = Message.objects.create(
            reply_to=self.message,
            text=text,
            user=ChatGTPUser,
            type=self.message.type
        )

    @classmethod
    def generate(cls):
        request_text = \
        f"""
        Напиши мне любое предложение или пару предложений на русском, которые я должен
        буду перевести на английский.
        """
        response_text = cls.get_response(request_text)
        new_message = Message.objects.create(
            text=response_text,
            user=ChatGTPUser,
            reply_to=None,
            type='pupil'
        )
        return new_message
