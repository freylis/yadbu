from ... import settings


def ya_auth(func):
    """
    Add headers about authorization with yandex oauth
    docs here: https://tech.yandex.ru/oauth/
    """
    def wrapper(*args, **kwargs):
        if kwargs.pop('with_auth', False):
            headers = kwargs.pop('headers', {})
            headers['Authorization'] = 'OAuth {}'.format(settings.YADBU_TOKEN)
            kwargs['headers'] = headers
        return func(*args, **kwargs)
    return wrapper
