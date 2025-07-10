def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


def format_ip_log(request, label='from IP', sep='='):
    ip = get_client_ip(request)
    return f'{label}{sep}{ip}'
