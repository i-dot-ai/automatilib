from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def hello_world(request):
    return HttpResponse("Hello, world")


def fake_login(request):
    return HttpResponse("you are logged in")
