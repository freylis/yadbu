from . import requester


def get_disk_info():
    response_data = requester.get('')
    return {
        'total_space': response_data['total_space'],
        'used_space': response_data['used_space'],
        'trash_space': response_data['trash_size'],
    }
