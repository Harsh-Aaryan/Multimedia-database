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


CREATE VIEW full_renting AS
    SELECT r.id, r.start_time_posix, r.end_time_posix, r.time_returned_posix, u.username, u.email AS user_email, m.id AS media_id, m.time_added_posix, m.title, m.release_year
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

--random data for bd populate
--0 root
--1 admin
--2 user
--3 viewer only

--book
-- INSERT INTO media (id, time_added_posix, title, release_year) VALUES
--     (200,1678991,'harry potter',1997),
--     (201,1678992,'harry potter 2',1998),
--     (202,1678993,'Dune',1984),
--     (204,1678994, '1984', 1949);

-- -- book infoo
-- INSERT INTO book (media_id, author, publisher, isbn) VALUES
--     (200, 'JK Rowling', 'Bloomsbury', '978-3-16-148410-0'),
--     (201, 'JK Rowling', 'Bloomsbury', '978-3-15-148410-1'),
--     (202, 'Frank Herbert', 'randomred', '978-5-16-148410-2'),
--     (204, 'George Orwell', 'Penguin', '978-4-16-148410-4');

-- --movie
-- INSERT INTO media (id, time_added_posix, title, release_year) VALUES
--     (300,1678997,'the lord of the rings',1997),
--     (301,1678998,'star wars',1998),
--     (302,1687998,'matrix',1999),
--     (304,1687999, 'star trek', 1979);

-- -- movie info
-- INSERT INTO movie (media_id, director, publisher, genre, duration_seconds) VALUES
--     (300, 'Peter Jackson', 'Sony', 'Fantasy', 180),
--     (301, 'George Lucas', 'Disney', 'Fantasy', 180),
--     (302, 'Lana Wachowski', 'Sony', 'Fantasy', 180),
--     (304, 'James Cameron', 'Sony', 'Fantasy', 180);

-- --music
-- INSERT INTO media (id, time_added_posix, title, release_year) VALUES
--     (400,1678999,'Graduation',2007),
--     (401,1678990,'Donda',2022),
--     (402,6789991,'A head full of dreams',2015);

-- -- music info
-- INSERT INTO music (media_id, artist, album, genre, duration_seconds) VALUES
--     (400, 'Kanye West', 'Graduation', 'Rap', 180),
--     (401, 'Kanye West', 'Donda', 'Rap', 180),
--    (402, 'Coldplay', 'A head full of dreams', 'Pop', 180);

-- -- need rental data
-- INSERT INTO renting (id, user_id, media_id, start_time_posix, end_time_posix, time_returned_posix) VALUES

--     (1, 3, 200, 1699987200, 1702579200, 1700592000),
--     (2, 4, 201, 1699987200, 1702579200, 9223372036854775807),
--     (4, 3, 204, 1696291200, 1698883200, 9223372036854775807),
--     (5, 4, 300, 1699987200, 1702579200, 1700592000),
--     (6, 5, 301, 1699987200, 1702579200, 9223372036854775807);
