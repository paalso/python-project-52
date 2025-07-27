from django.http import JsonResponse
from django.views import View

from task_manager.utils.debug import get_debug_info


class DebugInfoView(View):
    def get(self, request):
        debug_info = get_debug_info(request)
        return JsonResponse(debug_info)
