#Django imports
from django.http import JsonResponse
from django.views import View


# Create your views here.
class HelloHaikyuu(View):
    def get(self, request):
        return JsonResponse({"ok":True,"message": "Haikyuu. Miau", "data":[]},status=200)