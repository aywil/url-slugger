class DatabaseError(Exception):
    pass


class NotFoundSlugError(DatabaseError):
    pass


class NotFoundStatisticsError(DatabaseError):
    pass
