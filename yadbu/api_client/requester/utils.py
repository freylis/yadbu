import requests

from ... import errors
from . import decorators


URL = 'https://cloud-api.yandex.net/v1/disk/'


_errors_mapping = {
    400: errors.BadData,
    403: errors.Forbidden,
    404: errors.NotFound,
    409: errors.Conflict,
}


@decorators.ya_auth
@decorators.wrap_errors
def get(url, params=None, **kwargs):
    response = requests.get(URL + url, params=params, **kwargs)
    _handle_responses(response)
    return response.json()


@decorators.ya_auth
@decorators.wrap_errors
def put(url, params=None, absolute_url=False, **kwargs):
    request_url = url if absolute_url else URL + url
    response = requests.put(request_url, data=params, **kwargs)
    _handle_responses(response)
    return response.json() if response.text != '' else None


@decorators.ya_auth
@decorators.wrap_errors
def post(url, params=None, json=None, **kwargs):
    return requests.post(
        URL + url,
        data=params,
        json=json,
        **kwargs
    )


@decorators.ya_auth
@decorators.wrap_errors
def delete(url, **kwargs):
    return requests.delete(URL + url, **kwargs)


def _handle_responses(response):
    if response.status_code < 300:
        return
    if response.status_code >= 500:
        raise errors.InteranalYaDError(response.reason, error_data=response.text)
    if response.status_code in _errors_mapping:
        raise _errors_mapping[response.status_code](response.reason, error_data=response.json())
