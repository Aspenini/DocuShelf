const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();
const port = 8000;

// Set up storage for uploaded PDFs
const upload = multer({ dest: 'uploads/' });

// Database Setup
const db = new sqlite3.Database('./docushelf.db');

db.serialize(() => {
    db.run(`
        CREATE TABLE IF NOT EXISTS pdfs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            path TEXT
        )
    `);
});

// Upload Endpoint
app.post('/upload', upload.single('file'), (req, res) => {
    const { file } = req;
    if (!file) {
        return res.status(400).send('No file uploaded.');
    }

    // Save the uploaded file info into SQLite
    const title = file.originalname;
    const filePath = path.join('uploads', file.filename);
    db.run(
        `INSERT INTO pdfs (title, path) VALUES (?, ?)`,
        [title, filePath],
        function (err) {
            if (err) {
                return res.status(500).send('Error saving to database.');
            }
            res.status(200).send({ id: this.lastID, title, path: filePath });
        }
    );
});

// Get All PDFs Endpoint
app.get('/pdfs', (req, res) => {
    db.all(`SELECT * FROM pdfs`, (err, rows) => {
        if (err) {
            return res.status(500).send('Error retrieving PDFs.');
        }
        res.json(rows);
    });
});

// Endpoint to serve the PDF files
app.get('/uploads/:filename', (req, res) => {
    const { filename } = req.params;
    const filePath = path.join(__dirname, 'uploads', filename);
    if (fs.existsSync(filePath)) {
        res.sendFile(filePath);
    } else {
        res.status(404).send('File not found.');
    }
});

// Start the server
app.listen(port, () => {
    console.log(`DocuShelf backend listening at http://localhost:${port}`);
});
