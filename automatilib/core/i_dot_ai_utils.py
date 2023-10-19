from django.http import HttpResponseNotAllowed


class MethodDispatcher:
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

    def __new__(cls, request, *args, **kwargs):
        view = super().__new__(cls)
        method_name = request.method.lower()
        methods = {
            "get": view.get,
            "post": view.post,
        }
        method = methods.get(method_name, None)
        if method:
            return method(request, *args, **kwargs)
        else:
            return HttpResponseNotAllowed(request)
