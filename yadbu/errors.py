class YaDBuError(Exception):
    """Base Yandex.Disk backup tool exception"""
    pass


class ConnectionError(YaDBuError):
    """
    timeouts, connection errors, etc
    """


class BadData(YaDBuError):
    """
    400 from requester
    """


class Forbidden(YaDBuError):
    """
    403 from requester
    """


class NotFound(YaDBuError):
    """
    404 from requester
    """


class InteranalYaDError(YaDBuError):
    """
    Shit happens
    """


class Conflict(YaDBuError):
    """
    File or directory already exists
    """
