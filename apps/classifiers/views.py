from django.http import JsonResponse
from rest_framework.decorators import api_view
from howtoquant.utils import dict_fetch_all

from .db.queries import organization_types_select_all

@api_view(['GET'])
def org_types(request):
    if request.method == 'GET':
        data = dict_fetch_all(organization_types_select_all)
        return JsonResponse({'status': "OK", 'data': {"org_types": data}}, safe=False)
