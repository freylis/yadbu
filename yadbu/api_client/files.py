import os
import functools

from .. import errors
from . import requester


def upload_file(destination, file_path):
    # first, create directory with path
    filepath_parts = list(filter(
        lambda part: part,
        file_path.split(os.path.sep)
    ))
    file_directory = os.path.join(
        destination,
        *filepath_parts[:-1]
    )
    create_folder(file_directory)

    future_file_full_path = os.path.join(
        file_directory,
        filepath_parts[-1],
    )

    # second, get url to future file
    url_to_upload = _get_new_url(future_file_full_path)

    # third, upload file
    _upload_file(url_to_upload, file_path)


def create_folder(folder_name):
    path_parts = folder_name.split('/')
    path = ''
    result = None
    for part in path_parts:
        path += '{}/'.format(part)
        try:
            result = _create_subpath(path)
        except errors.Conflict:
            pass
    return result


def _create_subpath(path):
    url = 'resources/?path=app:/{}'.format(path)
    return requester.put(url)


def _get_new_url(future_file_full_path):
    params = {
        'path': 'app:/{}'.format(future_file_full_path),
    }
    feature_file_data = requester.get('resources/upload', params=params)
    return feature_file_data['href']


def _upload_file(url_to_upload, file_path):
    path_parts = file_path.split(os.path.sep)
    with open(file_path, 'rb') as f:
        response = requester.put(
            url_to_upload,
            absolute_url=True,
            files={
                path_parts[-1]: f,
            },
        )
    a = 1