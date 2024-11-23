const express = require('express');
const bodyParser = require('body-parser');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
const port = 3000;

// PostgreSQL pool
const pool = new Pool({
    user: 'test_1',
    host: 'localhost',
    database: 'sample_project',
    password: 'test',
    port: 5432,
});

app.use(cors());
app.use(express.json());

app.get('/search', async (req, res) => {
    // query 
    const { query, category } = req.query;

    let sqlQuery = 'SELECT media.title, media.release_year, ';
    let params = [ `%${query}%` ]; // searching 

    // SQL query based on the category
    if (category === 'book') {
        sqlQuery += 'book.author AS author, book.publisher AS publisher, book.isbn AS isbn, NULL AS genre, NULL AS duration_seconds ';
        sqlQuery += 'FROM media ';
        sqlQuery += 'JOIN book ON media.id = book.media_id ';
        sqlQuery += 'WHERE book.author ILIKE $1 OR book.publisher ILIKE $1 OR book.isbn ILIKE $1';
    } else if (category === 'movie') {
        sqlQuery += 'movie.director AS director, movie.publisher AS publisher, movie.genre AS genre, movie.duration_seconds ';
        sqlQuery += 'FROM media ';
        sqlQuery += 'JOIN movie ON media.id = movie.media_id ';
        sqlQuery += 'WHERE movie.director ILIKE $1 OR movie.publisher ILIKE $1 OR movie.genre ILIKE $1';
    } else if (category === 'music') {
        sqlQuery += 'music.artist AS artist, music.publisher AS publisher, music.album AS album, music.genre AS genre, music.duration_seconds ';
        sqlQuery += 'FROM media ';
        sqlQuery += 'JOIN music ON media.id = music.media_id ';
        sqlQuery += 'WHERE music.artist ILIKE $1 OR music.publisher ILIKE $1 OR music.album ILIKE $1 OR music.genre ILIKE $1';
    } else {
        // Search all nw
        sqlQuery += 'book.author AS author, book.publisher AS publisher, book.isbn AS isbn, NULL AS genre, NULL AS duration_seconds ';
        sqlQuery += 'FROM media ';
        sqlQuery += 'JOIN book ON media.id = book.media_id ';
        sqlQuery += 'WHERE book.author ILIKE $1 OR book.publisher ILIKE $1 OR book.isbn ILIKE $1';
        sqlQuery += ' UNION ';
        sqlQuery += 'SELECT media.title, media.release_year, movie.director AS director, movie.publisher AS publisher, movie.genre AS genre, movie.duration_seconds ';
        sqlQuery += 'FROM media ';
        sqlQuery += 'JOIN movie ON media.id = movie.media_id ';
        sqlQuery += 'WHERE movie.director ILIKE $1 OR movie.publisher ILIKE $1 OR movie.genre ILIKE $1';
        sqlQuery += ' UNION ';
        sqlQuery += 'SELECT media.title, media.release_year, music.artist AS artist, music.publisher AS publisher, music.album AS album, music.genre AS genre, music.duration_seconds ';
        sqlQuery += 'FROM media ';
        sqlQuery += 'JOIN music ON media.id = music.media_id ';
        sqlQuery += 'WHERE music.artist ILIKE $1 OR music.publisher ILIKE $1 OR music.album ILIKE $1 OR music.genre ILIKE $1';
    }

    try {
        const result = await pool.query(sqlQuery, params);
        res.status(200).json(result.rows); // Send results!!!!!
    } catch (error) {
        console.error(error);
        res.status(500).send('Database error');
    }
});



// server statt 
app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
