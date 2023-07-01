from celery import shared_task

import openai


@shared_task()
def get_response(text: str):
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}]
    )
    return result.choices[0].message.content
