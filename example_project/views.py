from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def hello_world(request):
    return HttpResponse("Hello, world")


@login_required
def my_account(request):
    return HttpResponse(f"welcome back {request.user.email}")


def login_failure(_):
    return HttpResponse("go away!", status=401)
