from task_manager.utils.debug import (
    detect_hosting_provider,  # путь к твоей функции
)


def hosting_provider(request):
    host = request.get_host()
    return {
        'hosting_provider': detect_hosting_provider(host) or {}
    }
