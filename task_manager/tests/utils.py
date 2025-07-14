import random

from django.contrib.messages import get_messages


def get_random_record(model):
    return random.choice(model.objects.all())


def extract_messages(response):
    return [str(m) for m in get_messages(response.wsgi_request)]


def assert_redirected_with_message(response, expected_url, message):
    assert response.status_code == 200
    assert response.redirect_chain
    last_redirect_url = response.redirect_chain[-1][0]
    assert last_redirect_url == expected_url
    messages = extract_messages(response)
    assert any(message in m for m in messages),\
        f'Message "{message}" not found in {messages}'
