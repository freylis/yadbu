from . import requester


def get_disk_info():
    response_data = requester.get(
        '',
        with_auth=True,
    )
    return response_data
