import logging

from django.shortcuts import render
from django.views import View

logger = logging.getLogger(__name__)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        logger.info(f'User: {user}, authenticated: {user.is_authenticated}')
        return render(request, 'index.html')
