from django.middleware.csrf import get_token
from django.http import JsonResponse

def fetchCSRFToken(request):
    token = get_token(request)
    return JsonResponse({'csrf_token': token}) 