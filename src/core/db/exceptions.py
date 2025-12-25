class DatabaseError(Exception):
    pass


class NotFoundSlugError(DatabaseError):
    pass


class NotFoundStatisticsError(DatabaseError):
    pass


class CustomSlugError(DatabaseError):
    pass


class InvalidUrlError(DatabaseError):
    pass
