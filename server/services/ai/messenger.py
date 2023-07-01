import dataclasses
import os
import re
from typing import Any
from django.db.utils import IntegrityError, OperationalError
import openai
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import ThreadPool

from openai.error import AuthenticationError

from users.models import Account
from chats.models import Message
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
    ChatGTPUser = Account.objects.create_chatgpt_account()
    ChatGTPUser.score = 6000
    ChatGTPUser.save()


try:
    create_gpt_user()
except IntegrityError:  # instance exists, it`s OK
    ChatGTPUser = Account.objects.get(user__username='chat-gpt')
    # ChatGTPUser.delete()
    # create_gpt_user()
except OperationalError as error:
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


@dataclasses.dataclass
class MessageData:
    text: str
    type: str


class Messenger(ChatGPT):
    __slots__ = ('message', 'func')
    user = ChatGTPUser
    score_pattern: re.Pattern = re.compile(r"\((\d\d?)\)")

    def __init__(self, message: Message):
        super().__init__()
        self.message = message

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

    def save_answer(self, text: str) -> Message:
        scores = self.find_score(text)
        if scores is not None:
            self.message.sender.add_score(scores)
        answer_message = Message.objects.create(
            text=text,
            sender=ChatGTPUser,
            type=self.message.type,
            chat=self.message.chat
        )
        return answer_message

    @classmethod
    def generate(cls, chat):
        request_text = \
            f"""
            Напиши мне любое предложение или пару предложений на русском, которые я должен
            буду перевести на английский.
            """
        response_text = cls.get_response(request_text)
        new_message = Message.objects.create(
            text=response_text,
            sender=ChatGTPUser,
            chat=chat,
            type='pupil'
        )
        return new_message
