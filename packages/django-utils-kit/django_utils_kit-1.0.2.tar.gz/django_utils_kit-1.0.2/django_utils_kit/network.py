"""Network related utilities to handle requests."""

from django.conf import settings
from django.http import HttpRequest


def get_client_ip(request: HttpRequest) -> str:
    """
    Gets the client IP address from the request.

    Args:
        request (HttpRequest): The request object.

    Returns:
        str: The client IP address.
    """
    if request.META.get("HTTP_X_FORWARDED_FOR"):
        return request.META.get("HTTP_X_FORWARDED_FOR").split(",")[-1].strip()
    elif request.META.get("HTTP_X_REAL_IP"):
        return request.META.get("HTTP_X_REAL_IP")
    return request.META.get("REMOTE_ADDR")


def get_server_domain(default: str = "http://127.0.0.1:8000/") -> str:
    """
    Gets the server domain from the settings.

    Args:
        default (str, optional): The default domain. Defaults to "http://127.0.0.1:8000/".

    Returns:
        str: The server domain.
    """
    hosts = settings.ALLOWED_HOSTS
    domain = hosts[0] if hosts else default
    return domain
