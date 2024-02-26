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
    const amazonData = await getScrapedData('http://127.0.0.1:5001/amazon', search_term);
    // console.log('Amazon Data:', amazonData);

    const flipkartData = await getScrapedData('http://127.0.0.1:5001/flipkart', search_term);
    // console.log('Flipkart Data:', flipkartData);

    if (category === 'lifestyle') { 
         myntraData = await getScrapedData('http://127.0.0.1:5001/myntra', search_term);
        // console.log('Myntra Data:',myntraData);
    }
    // Pass userId to the template
    const userId = req.session.userId;
    
    // Render the results page with data and userId
    res.render(path.join(__dirname, 'views', 'results.ejs'), { amazonData, flipkartData, myntraData, userId });
});

app.get('/goBack', (req, res) => {
    // res.send('<script>window.history.back(-1);</script>');
    res.redirect('back');
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

app.post('/wishlist/add', async (req, res) => {
    const userId = req.session.userId;
    const { name, price, link, image_link } = req.body;

    const trimmedName = name.trim();
    const trimmedPrice = price.trim().replace('₹', 'Rs. ');
    const trimmedLink = link.trim();
    const trimmedImageLink = image_link.trim();

    // console.log('Received request to add product to wishlist:', { userId, trimmedName, trimmedPrice, trimmedLink, trimmedImageLink });
    
    try {

        const [result] = await db.promise().query('INSERT INTO wishlisted_products (user_id, name, price, link, image_link) VALUES (?, ?, ?, ?, ?)',
            [userId, trimmedName, trimmedPrice, trimmedLink, trimmedImageLink]);

            const productId = result.insertId; 
            res.status(200).json({ success: true, message: 'Product added to wishlist successfully', productId });
    } catch (error) {
        console.error('Error adding product to wishlist:', error);
        res.status(500).send('Failed to add product to wishlist.');
    }
});



app.post('/wishlist/remove', async (req, res) => {
    const userId = req.session.userId;
    const productId = req.body.productId;

    try {
        await db.execute('SET SQL_SAFE_UPDATES=0');
        await db.execute('DELETE FROM wishlisted_products WHERE id = ? AND user_id = ?', [productId, userId]);

        res.status(200).json({ success: true }); 
    } catch (error) {
        console.error('Error removing product from wishlist:', error);
        res.status(500).json({ success: false });
    }
});


app.get('/wishlist', async (req, res) => {
    // try{
    const userId = req.session.userId;
    const [rows] = await db.promise().query('SELECT * FROM wishlisted_products WHERE user_id = ?', [userId]);
    if (!Array.isArray(rows)) {
        throw new Error('Query result is not iterable');
    }
    console.log('Wishlisted Products Rows:', rows);
    // res.render(path.join(__dirname, 'views', 'wishlist.ejs'), { amazonData, flipkartData, myntraData, userId });
    res.render('wishlist', { wishlistedProducts: rows });
    // }catch (error) {
    //     console.error('Error fetching or rendering wishlisted products:', error);
    //     res.status(500).send('Internal Server Error');
    // }
});



app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});








