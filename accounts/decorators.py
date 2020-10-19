from django.shortcuts import redirect
from django.http import HttpResponse


def unauthenticated(func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return func(request, *args, **kwargs)
    return wrapper_func


def allowed_group(allowed=[]):
    def decorator(func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed:
                return func(request, *args, **kwargs)
            else:
                return HttpResponse("You're not allowed in this page")
        return wrapper_func
    return decorator


def admin_only(func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == "customer":
            return redirect("user_page")

        if group == "admin":
            return func(request, *args, **kwargs)

    return wrapper_func
