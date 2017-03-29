import requests

from ... import errors
from ... import settings


def ya_request_params(func):
    """
    Add headers about authorization with yandex oauth
    docs here: https://tech.yandex.ru/oauth/
    """
    def wrapper(*args, **kwargs):
        # authorization
        if kwargs.pop('with_auth', True):
            headers = kwargs.pop('headers', {})
            headers['Authorization'] = 'OAuth {}'.format(settings.YADBU_TOKEN)
            kwargs['headers'] = headers

        # request timeout
        if 'timeout' not in kwargs:
            kwargs['timeout'] = settings.YADBU_REQUEST_TIMEOUT
        return func(*args, **kwargs)
    return wrapper


def wrap_errors(func):
    """
    Replace errors to yadbu exceptions
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.RequestException as exc:
            raise errors.ConnectionError(str(exc)) from exc
    return wrapper
