from django.utils.deprecation import MiddlewareMixin
from .conf import UTM_PARAMETERS

class UTMMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == "GET":
            for param in UTM_PARAMETERS:
                value = request.GET.get(param)
                if value:
                    request.session[param] = value
