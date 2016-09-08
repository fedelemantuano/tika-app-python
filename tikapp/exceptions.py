__all__ = [
    "InvalidTikaAppJar",
    "InvalidSwitches",
    "InvalidFilePath",
    "InvalidParameters",
    "TempIOError",
]


class InvalidTikaAppJar(ValueError):
    pass


class InvalidSwitches(ValueError):
    pass


class InvalidFilePath(ValueError):
    pass


class InvalidParameters(ValueError):
    pass


class TempIOError(Exception):
    pass
