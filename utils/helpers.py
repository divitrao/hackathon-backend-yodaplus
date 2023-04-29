from rest_framework.response import Response
from cryptography.fernet import Fernet
from django.conf import settings


def get_or_none_for_manager(manager, select_related=[], **kwargs):
    # common get or none logic extended by all
    # other get or none utils
    # using .last() instead of .first() because old logic used the same

    queryset = manager.filter(**kwargs)

    if select_related:
        queryset = queryset.select_related(*select_related)

    try:
        return queryset.last()
    except (
        manager.model.DoesNotExist,
        ValueError,
        TypeError,
        IndexError,
    ):
        return None


def get_or_none(model, select_related=[], **kwargs):
    return get_or_none_for_manager(model.objects, select_related=select_related, **kwargs)


def error_response(status, msg, data, *args, **kwargs):
    response = {
        "status_code": status,
        "status": "failure",
        "detail": msg,
        "data": data,
    }
    caller_func = kwargs.get("caller_func", None)
    return Response(data=response, status=status)


def success_response(status, msg, data, *args, **kwargs):
    response = {
        "status_code": status,
        "status": "success",
        "detail": msg,
        "data": data,
    }
    return Response(data=response, status=status)



def encrypt(password):
    key = bytes(settings.FERNET_KEY,'utf-8')
    f = Fernet(key)
    return f.encrypt(bytes(password,'utf-8'))

def decrypt(password):
    key = bytes(settings.FERNET_KEY,'utf-8')
    f = Fernet(key)
    return f.decrypt(password)