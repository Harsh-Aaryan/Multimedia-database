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

--connection
\c multimedia_db


CREATE TABLE user_data (
    id INTEGER PRIMARY KEY,
    username VARCHAR(1024) UNIQUE,
    email VARCHAR(1024) UNIQUE,
    password VARCHAR(1024),
    access_level INTEGER
);

CREATE TABLE media (
    id INTEGER PRIMARY KEY,
    time_added_posix BIGINT,
    title VARCHAR(1024),
    release_year INTEGER
);

CREATE TABLE renting (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES user_data(id) ON DELETE CASCADE,
    media_id INTEGER REFERENCES media(id) ON DELETE SET NULL,
    start_time_posix BIGINT,
    end_time_posix BIGINT,
    time_returned_posix BIGINT
    CHECK (end_time_posix > start_time_posix AND time_returned_posix > start_time_posix)
);

CREATE TABLE book (
    media_id INTEGER PRIMARY KEY REFERENCES media(id) ON DELETE CASCADE,
    author VARCHAR(1024),
    publisher VARCHAR(1024),
    isbn VARCHAR(32) NOT NULL UNIQUE
);

CREATE TABLE movie (
    media_id INTEGER PRIMARY KEY REFERENCES media(id) ON DELETE CASCADE,
    director VARCHAR(1024),
    publisher VARCHAR(1024),
    genre VARCHAR(1024),
    duration_seconds INTEGER CHECK (duration_seconds > 0)
);

CREATE TABLE music (
    media_id INTEGER PRIMARY KEY REFERENCES media(id) ON DELETE CASCADE,
    artist VARCHAR(1024),
    publisher VARCHAR(1024),
    album VARCHAR(1024),
    genre VARCHAR(1024),
    duration_seconds INTEGER CHECK (duration_seconds > 0)
);


CREATE VIEW total_overdue_media AS
    SELECT user_id, COUNT(user_id) AS overdue_media
    FROM renting
    WHERE (time_returned_posix != 9223372036854775807 AND time_returned_posix > end_time_posix) OR (time_returned_posix = 9223372036854775807 and end_time_posix < trunc(extract(epoch from now() )* 1000))
    GROUP BY user_id
;

CREATE VIEW full_user AS
    SELECT u.id, u.username, u.email, u.password, u.access_level, COALESCE(t.overdue_media, 0) AS overdue_media
    FROM user_data AS u LEFT JOIN total_overdue_media AS t ON u.id = t.user_id
;

CREATE VIEW full_renting AS
    SELECT r.id, r.start_time_posix, r.end_time_posix, r.time_returned_posix, u.id AS user_id, u.username, u.email AS user_email, m.id AS media_id, m.time_added_posix, m.title, m.release_year
    FROM user_data AS u JOIN renting AS r ON u.id = r.user_id JOIN media AS m ON r.media_id = m.id
;

CREATE VIEW full_book AS
    SELECT m.id, m.time_added_posix, m.title, m.release_year, b.author, b.publisher, b.isbn
    FROM media AS m JOIN book AS b ON m.id = b.media_id
;

CREATE VIEW full_movie AS
    SELECT m.id, m.time_added_posix, m.title, m.release_year, o.director, o.publisher, o.genre, o.duration_seconds
    FROM media AS m JOIN movie AS o ON m.id = o.media_id
;

CREATE VIEW full_music AS
    SELECT m.id, m.time_added_posix, m.title, m.release_year, u.artist, u.publisher, u.album, u.genre, u.duration_seconds
    FROM media AS m JOIN music AS u ON m.id = u.media_id
;
