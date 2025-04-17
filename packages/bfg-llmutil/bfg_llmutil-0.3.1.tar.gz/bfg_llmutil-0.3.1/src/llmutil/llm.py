import json

from openai import OpenAI

from .client import default_client


def chat(messages, model="gpt-4o", client=None, **kwargs):
    assert isinstance(messages, list) and len(messages) > 0
    assert isinstance(model, str)
    assert isinstance(client, OpenAI) or client is None

    if client is None:
        client = default_client()

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        **kwargs,
    )
    return response.choices[0].message.content


def gen(sysmsg, usrmsg, response_format, model="gpt-4o", client=None, **kwargs):
    assert isinstance(sysmsg, str)
    assert isinstance(usrmsg, str)
    assert isinstance(response_format, dict)
    assert isinstance(model, str)
    assert isinstance(client, OpenAI) or client is None

    if client is None:
        client = OpenAI()

    messages = [
        {"role": "system", "content": sysmsg},
        {"role": "user", "content": usrmsg},
    ]
    response = client.beta.chat.completions.parse(
        model=model,
        messages=messages,
        response_format=response_format,
        **kwargs,
    )
    return json.loads(response.choices[0].message.content)


def ask(instructions, question):
    response = default_client().responses.create(
        model="gpt-4o",
        input=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": question},
        ],
    )
    return response.output_text
