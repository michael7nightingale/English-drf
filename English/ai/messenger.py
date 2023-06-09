import os
import re
from typing import Any
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError, OperationalError
import openai
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import ThreadPool
import sys

from openai.error import AuthenticationError

sys.path.append('d:/Progs/PycharmProjects/English/English')
from api.models import Message
from .tasks import get_response


pool = ThreadPool()
executor = ThreadPoolExecutor()


openai_key = os.environ.get('OPENAI_KEY')
if openai_key is None:
    raise ValueError("OpenAI key expected.")
try:
    ...
except AuthenticationError:
    raise ValueError("OpenAI key exists, but not valid. Check your key")
openai.api_key = openai_key


ChatGTPUser = None


def create_gpt_user() -> None:
    global ChatGTPUser
    ChatGTPUser = get_user_model().objects.create(
        username='chat-gpt',
        password='chat-gpt-password',
        location='New York',
        level='C2',
        email='chat_gpt@mail.ru',
        score=6000,
    )


try:
    create_gpt_user()
except IntegrityError:  # instance exists, it`s OK
    ChatGTPUser = get_user_model().objects.get(username='chat-gpt')
    # ChatGTPUser.delete()
    # create_gpt_user()
except OperationalError as error:
    print(str(error))
    print("Need migrations")


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
    score_pattern: re.Pattern = re.compile(r"\((\d\d?)\)")

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

    def find_score(self, text: str) -> int | None:
        match = self.score_pattern.findall(text)
        if match:
            scores = match[0]
            if scores.isdigit():
                return int(scores)
        return None

    def __reply_to_remark(self) -> str:
        text = \
            f"""
                Побудь моим учителем английского и редактором сообщения.
                Вот мой текст: {self.message.text}
                Исправь в нем ошибки и объясни, в чём я ошибся. Если я всё сделал правильно, то похвали.
                В конце сообщения напиши в скобках единственное число от 0 до 10 - объективная оценка моего сообщения на 
                уровень владения конкретно английским языком, например: (5). Оцени белеберду в 0 баллов.
            """
        return text.strip().replace('\n', ' ')

    def __reply_to_pupil(self) -> str:
        original_message = self.message.reply_to
        text = \
            f"""
                Побудь моим учителем английского и редактором сообщения.
                Я должен был перевести на английский язык этот текст: {original_message.text}.
                Вот мой перевод: {self.message.text}
                Исправь в нем ошибки и объясни, в чём я ошибся. 
                Если я всё сделал правильно, то не похвали. В конце сообщения напиши в скобках единственное число от 0 до 10 - объективная 
                оценка моего перевода.
            """
        return text.strip().replace('\n', ' ')

    def save_answer(self, text: str) -> None:
        scores = self.find_score(text)
        if scores is not None:
            self.message.user.add_score(scores)
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
