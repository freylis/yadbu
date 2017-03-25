ERROR_BAD_DATA = 1400
ERROR_FORBIDDEN = 1403
ERROR_NOT_FOUND = 1404
ERROR_UNKNOWN = 1500
ERROR_CONNECTION_ERROR = 1600


class YaDBuError(Exception):
    """Base Yandex.Disk backup tool exception"""
    DEFAULT_CODE = ERROR_UNKNOWN

    def __init__(self, *args, error_data=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._error_data = error_data

    def get_msg(self):
        return str(self)

    @property
    def error_code(self):
        return self.DEFAULT_CODE


class ConnectionError(YaDBuError):
    DEFAULT_CODE = ERROR_CONNECTION_ERROR

    def get_msg(self):
        return 'Ошибкая соединения с yandex.disk'


class BadData(YaDBuError):
    DEFAULT_CODE = ERROR_BAD_DATA


class Forbidden(YaDBuError):
    DEFAULT_CODE = ERROR_FORBIDDEN


class NotFound(YaDBuError):
    DEFAULT_CODE = ERROR_NOT_FOUND


class InteranalYaDError(YaDBuError):
    DEFAULT_CODE = ERROR_UNKNOWN
