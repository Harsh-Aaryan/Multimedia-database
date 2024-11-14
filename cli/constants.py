CONFIG_PATH = "config.json"
DEFAULT_CONFIG = {
    "user_id": -1
}

RETURN_TIME_DAYS = 30
RETURN_TIME_SECONDS = 60 * 60 * 24 * RETURN_TIME_DAYS

TABLE_MAPPING = {
    "account": "user_data",
    "book": "full_book",
    "media": "media",
    "movie": "full_movie",
    "music": "full_music"
}

COLUMN_MAPPING = {
    "album": "album",
    "artist": "artist",
    "author": "author",
    "date-added": "time_added_posix",
    "director": "director",
    "duration": "duration_seconds",
    "email": "email",
    "genre": "genre",
    "id": "id",
    "isbn": "isbn",
    "password": "password",
    "publisher": "publisher",
    "release-year": "release_year",
    "title": "title",
    "username": "username"
}

OPERATORS = [   #   Python; SQL
    ":",        #   in      like
    "<",        #   <       <
    "=",        #   ==      =
    ">"         #   >       >
]

DATABASE_NAME = "multimedia_db"
DATABASE_USER = "postgres"
POSTGRES_MAX_INTEGER_SIZE = 2147483647
POSTGRES_MAX_BIGINT_SIZE = 9223372036854775807
