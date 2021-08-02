from django.http import HttpResponseForbidden


class FilterIPMiddleware(object):
    def __init__(self, get_response):
        """
        One-time configuration and initialisation.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before the view (and later
        middleware) are called.
        """
        edameh = False
        ip = request.META.get('REMOTE_ADDR')  # Get client IP
        arr_ip = ip.split(".")
        if (arr_ip[0] == "192" or arr_ip[0] == "127") and (arr_ip[1] == "168" or arr_ip[1] == "0") :
            edameh = True
        else:
            full_path = request.get_full_path()
            if (full_path.find('api/token') > -1 or full_path.find('api/bazdidkhodro/') > -1 or full_path.find('/admin') > -1 or full_path.find('/install') > -1):
                edameh = True

        if edameh == False:
            return HttpResponseForbidden('Access Denied')

        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Called just before Django calls the view.
        """
        return None

    def process_exception(self, request, exception):
        """
        Called when a view raises an exception.
        """
        return None

    def process_template_response(self, request, response):
        """
        Called just after the view has finished executing.
        """
        return response
