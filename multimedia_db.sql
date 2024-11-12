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
    username CHAR(80),
    email CHAR(80),
    password CHAR(80),
    access_level INTEGER
);

CREATE TABLE media (
    id INTEGER PRIMARY KEY,
    time_added_posix INTEGER,
    title CHAR(80),
    release_year INTEGER
);

CREATE TABLE renting (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES user_data(id) ON DELETE CASCADE,
    media_id INTEGER REFERENCES media(id) ON DELETE SET NULL,
    start_time_posix INTEGER NOT NULL,
    end_time_posix INTEGER,
    CHECK (end_time_posix > start_time_posix)
);

CREATE TABLE book (
    media_id INTEGER PRIMARY KEY REFERENCES media(id) ON DELETE CASCADE,
    author CHAR(80),
    publisher CHAR(80),
    isbn CHAR(80) NOT NULL UNIQUE
);

CREATE TABLE movie (
    media_id INTEGER PRIMARY KEY REFERENCES media(id) ON DELETE CASCADE,
    director CHAR(80),
    publisher CHAR(80),
    genre CHAR(80),
    duration_seconds INTEGER CHECK (duration_seconds > 0)
);

CREATE TABLE music (
    media_id INTEGER PRIMARY KEY REFERENCES media(id) ON DELETE CASCADE,
    artist CHAR(80),
    album CHAR(80),
    genre CHAR(80),
    duration_seconds INTEGER CHECK (duration_seconds > 0)
);


CREATE VIEW full_book AS
    SELECT m.id, m.time_added_posix, m.title, m.release_year, b.author, b.publisher, b.isbn
    FROM media AS m JOIN book AS b ON m.id = b.media_id
;


CREATE VIEW full_movie AS
    SELECT m.id, m.time_added_posix, m.title, m.release_year, o.director, o.publisher, o.genre, o.duration_seconds
    FROM media AS m JOIN movie AS o ON m.id = o.media_id
;


CREATE VIEW full_music AS
    SELECT m.id, m.time_added_posix, m.title, m.release_year, u.artist, u.album, u.genre, u.duration_seconds
    FROM media AS m JOIN music AS u ON m.id = u.media_id
;
