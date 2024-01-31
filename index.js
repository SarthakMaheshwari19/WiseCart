// server.js

const express = require('express');
const axios = require('axios');
const session = require('express-session');
const bcrypt = require('bcryptjs');
const mysql = require('mysql2');
const path = require('path');

const app = express();

const db = mysql.createPool({
    host: 'localhost',
    user: 'Sarthak',
    password: 'Sarthak@123',
    database: 'Login_info',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});
// console.log(db);

// Export the database connection and the app
module.exports = db.promise();

app.use(express.json());
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));

app.use(session({
    secret: 'secret',
    resave: false,
    saveUninitialized: false
}));


app.set('view engine', 'ejs');
// app.engine('html', require('ejs').renderFile);

app.use('/public', express.static(path.join(__dirname, 'public'))); 


app.use('/auth', require('./routes/auth'));
app.get('/auth', (req, res) => {
    res.render('auth');
});
app.use(function (req, res, next) {
    if (!req.session.userId) {
      return res.redirect('/auth');
    }
    next();
});
app.get('/logout', (req, res) => {
    req.session.destroy(err => {
        if (err) {
            console.error('Error destroying session:', err);
        } else {
            res.redirect('/auth');
        }
    });
});



app.get('/', (req, res) => {
    res.render('index');  
});

app.post('/search', async (req, res) => {
    const search_term = req.body.search;
    const category = req.body.category;
    let myntraData=[]
    // Call Python service for Amazon data
    const amazonData = await getScrapedData('http://127.0.0.1:5001/amazon', search_term);
    // console.log('Amazon Data:', amazonData);

    // Call Python service for Flipkart data
    const flipkartData = await getScrapedData('http://127.0.0.1:5001/flipkart', search_term);
    // console.log('Flipkart Data:', flipkartData);

    if (category === 'lifestyle') { 
         myntraData = await getScrapedData('http://127.0.0.1:5001/myntra', search_term);
        // console.log('Myntra Data:',myntraData);
    }

    // Render the results page with data
    res.render(path.join(__dirname, 'views', 'results.ejs'), { amazonData,flipkartData ,myntraData });
});

async function getScrapedData(apiEndpoint, search_term) {
    try {
        const response = await axios.get(apiEndpoint, { params: { term: search_term } });
        return response.data;
    } catch (error) {
        console.error(`Error fetching data from ${apiEndpoint}:`, error.message);
        return [];
    }
}

app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});








