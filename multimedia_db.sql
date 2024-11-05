-- Create the database itself (uncomment to create for the first time)
-- CREATE DATABASE multimedia_db
--     WITH
--     OWNER = postgres
--     ENCODING = 'UTF8'
--     LC_COLLATE = 'English_United States.1252'
--     LC_CTYPE = 'English_United States.1252'
--     LOCALE_PROVIDER = 'libc'
--     TABLESPACE = pg_default
--     CONNECTION LIMIT = -1
--     IS_TEMPLATE = False;

-- Empty the database (so you don't have to keep deleting and recreating manually)
DROP TABLE IF EXISTS BOOK CASCADE;
DROP TABLE IF EXISTS MOVIE CASCADE;
DROP TABLE IF EXISTS RENTING CASCADE;
DROP TABLE IF EXISTS MEDIA CASCADE;
DROP TABLE IF EXISTS USER_DATA CASCADE;


-- Create USER_DATA table
CREATE TABLE USER_DATA (
    id INTEGER PRIMARY KEY,
    username CHAR(80) NOT NULL,
    email CHAR(80),
    password CHAR(80) NOT NULL,
    access_level INTEGER
);

-- Create MEDIA table
CREATE TABLE MEDIA (
    id INTEGER PRIMARY KEY,
    title CHAR(80) NOT NULL,
    time_added_posix INTEGER NOT NULL,
    release_year INTEGER
);

-- Create RENTING table
CREATE TABLE RENTING (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES USER_DATA(id),
    media_id INTEGER REFERENCES MEDIA(id),
    start_time_posix INTEGER NOT NULL,
    end_time_posix INTEGER,
    CHECK (end_time_posix > start_time_posix)
);

-- Create BOOK table
CREATE TABLE BOOK (
    media_id INTEGER PRIMARY KEY REFERENCES MEDIA(id),
    author CHAR(80),
    publisher CHAR(80),
    isbn INTEGER NOT NULL UNIQUE
);

-- Create MOVIE table
CREATE TABLE MOVIE (
    media_id INTEGER PRIMARY KEY REFERENCES MEDIA(id),
    director CHAR(80),
    publisher CHAR(80)
);
