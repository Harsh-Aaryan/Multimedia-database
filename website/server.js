const express = require('express');
const bodyParser = require('body-parser');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
const port = 3000;

// created new pool
const pool = new Pool({
    user: 'test_1',
    host: 'localhost',
    database: 'sample_project',
    password: 'test',
    port: 5432,
});


app.use(cors());
app.use(bodyParser.json());

// endpoints for data
app.post('/register', async (req, res) => {
    const { username, email, password, access_level = 1 } = req.body; // default access  = 1

    try {
        const result = await pool.query(
            'INSERT INTO user_data (username, email, password, 1) VALUES ($1, $2, $3, $4) RETURNING id',
            [username, email, password, access_level]
        );
        res.status(200).send({ message: 'User registered successfully!', userId: result.rows[0].id });
    } catch (error) {
        console.error(error);
        if (error.code === '23505') {
            // constraint violation
            res.status(400).send({ error: 'Username or email already exists.' });
        } else {
            res.status(500).send({ error: 'Database error.' });
        }
    }
});

// to start 
app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
