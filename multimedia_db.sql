\c postgres

DROP DATABASE IF EXISTS multimedia_db;

CREATE DATABASE multimedia_db
    WITH OWNER = postgres
    ENCODING = 'UTF8'
    -- LC_COLLATE = 'English_United States.1252'
    -- LC_CTYPE = 'English_United States.1252'
    -- LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False
;

\c multimedia_db


CREATE TABLE user_data (
    id INTEGER PRIMARY KEY,
    username VARCHAR(1024) NOT NULL,
    email VARCHAR(1024),
    password VARCHAR(1024) NOT NULL,
    access_level INTEGER
);

CREATE TABLE media (
    id INTEGER PRIMARY KEY,
    title VARCHAR(1024) NOT NULL,
    time_added_posix BIGINT NOT NULL,
    release_year INTEGER
);

CREATE TABLE renting (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES user_data(id),
    media_id INTEGER REFERENCES media(id),
    start_time_posix BIGINT NOT NULL,
    end_time_posix BIGINT,
    CHECK (end_time_posix > start_time_posix)
);

CREATE TABLE book (
    media_id INTEGER PRIMARY KEY REFERENCES media(id),
    author VARCHAR(1024),
    publisher VARCHAR(1024),
    isbn INTEGER NOT NULL UNIQUE
);

CREATE TABLE movie (
    media_id INTEGER PRIMARY KEY REFERENCES media(id),
    director VARCHAR(1024),
    publisher VARCHAR(1024),
    genre VARCHAR(1024),
    duration_seconds INTEGER CHECK (duration_seconds > 0)
);

CREATE TABLE music (
    media_id INTEGER PRIMARY KEY REFERENCES media(id),
    artist VARCHAR(1024),
    album VARCHAR(1024),
    genre VARCHAR(1024),
    duration_seconds INTEGER CHECK (duration_seconds > 0)
);
