import requests

from . import decorators


URL = 'https://cloud-api.yandex.net/v1/disk/'


@decorators.ya_auth
def get(url, params=None, **kwargs):
    response = requests.get(URL + url, params=params, **kwargs)
    return response


@decorators.ya_auth
def put(url, params=None, **kwargs):
    return requests.put(URL + url, data=params, **kwargs)


@decorators.ya_auth
def post(url, params=None, json=None, **kwargs):
    return requests.post(
        URL + url,
        data=params,
        json=json,
        **kwargs
    )


@decorators.ya_auth
def delete(url, **kwargs):
    return requests.delete(URL + url, **kwargs)
