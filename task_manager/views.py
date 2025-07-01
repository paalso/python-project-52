import logging

from django.shortcuts import render

logger = logging.getLogger(__name__)


def index(request):
    user = request.user
    logger.info(f'User: {user}, authenticated: {user.is_authenticated}')
    return render(request, 'index.html')
