import random

from django.contrib.messages import get_messages


def get_random_record(model):
    return random.choice(model.objects.all())


def extract_messages(response):
    return [str(m) for m in get_messages(response.wsgi_request)]
