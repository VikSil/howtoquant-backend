import json
from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['GET'])
def api(request):

    if request.method == 'GET':
        f = open('howtoquant/assets/json/all_endpoints.json')
        data = json.load(f)
        return JsonResponse(data, safe=False)
