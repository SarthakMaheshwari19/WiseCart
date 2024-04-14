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


app.get('/', async (req, res) => {
    const userId = req.session.userId; // Assuming the user's ID is stored in the session
    let searchHistory = [];
    try {
        const [rows] = await db.promise().query('SELECT search_term FROM search_history WHERE user_id = ? ORDER BY search_date DESC LIMIT 10', [userId]);
        searchHistory = rows.map(row => row.search_term);
    } catch (error) {
        console.error('Error fetching search history:', error);
    }
    res.render('index', { searchHistory });
});
// app.get('/', (req, res) => {
//     res.render('index');  
// });

app.post('/search', async (req, res) => {
    console.log(req.body)
    const user_Id = req.session.userId; // Assuming the user's ID is stored in the session
    const searching_term = req.body.search || `${req.body.origin} to ${req.body.destination}`;
    // Insert search term and user ID into the database
    try {
        await db.promise().query('INSERT INTO search_history (search_term, user_id) VALUES (?, ?)', [searching_term, user_Id]);
    } catch (error) {
        console.error('Error saving search term to database:', error);
    } // Assuming the user's ID is stored in the session

    // const search_term = req.body.search;
    const category = req.body.category;
    let myntraData = [];
    let amazonData = [];
    let flipkartData = [];
    let paytmFlightsData = [];
    let makemytripData = [];

    if (category === 'electronics' || category === 'lifestyle') {
        const search_term = req.body.search;
        
        amazonData = await getScrapedData('http://127.0.0.1:5001/amazon', search_term);
        flipkartData = await getScrapedData('http://127.0.0.1:5001/flipkart', search_term);

        if (category === 'lifestyle') {
            myntraData = await getScrapedData('http://127.0.0.1:5001/myntra', search_term);
        }
    } else if (category === 'flights') {
        const origin = req.body.origin;
        const destination = req.body.destination;
        const departureDate = new Date(req.body.departureDate);
        const formattedDepartureDate = `${departureDate.getDate()}/${departureDate.getMonth() + 1}/${departureDate.getFullYear()}`;

        paytmFlightsData = await getFlightData('http://127.0.0.1:5001/paytmflights', { origin, destination, formattedDepartureDate });
        console.log('paytm flights Data:', paytmFlightsData);
        makemytripData = await getFlightData('http://127.0.0.1:5001/makemytrip', { origin, destination, formattedDepartureDate });
        console.log('make my trip flights Data:', makemytripData);
    }
    const userId = req.session.userId;
    
    // Render the results page with data and userId
    res.render(path.join(__dirname, 'views', 'results.ejs'), { amazonData, flipkartData, myntraData, paytmFlightsData, makemytripData, userId });
});

// Fetch user data by ID and render profile page with EJS
app.get('/profile', async (req, res) => {
    const userid  = req.session.userId;
    console.log('object',userid)
    try {
        const [rows] = await db.promise().query('SELECT * FROM users WHERE id = ?', [userid]);
        if (rows.length > 0) {
            res.render('profile', { user: rows[0] });
        } else {
            res.status(404).send('User not found');
        }
    } catch (error) {
        console.error('Error fetching user:', error);
        res.status(500).send('Internal Server Error');
    }
});

app.put('/profile/update', async (req, res) => {
    const userId = req.session.userId;
    const { name, email } = req.body;

    // Filter out null or undefined values
    const fieldsToUpdate = { name, email };
    Object.keys(fieldsToUpdate).forEach(key => fieldsToUpdate[key] == null && delete fieldsToUpdate[key]);

    // Build the SET part of the SQL query
    const setPart = Object.keys(fieldsToUpdate).map(key => `${key} = ?`).join(', ');

    // Build the values array for the query
    const values = Object.values(fieldsToUpdate);
    values.push(userId); // Add the userId for the WHERE clause

    try {
        const [result] = await db.promise().query(`UPDATE users SET ${setPart} WHERE id = ?`, values);
        if (result.affectedRows > 0) {
            res.send('User updated successfully');
        } else {
            res.status(404).send('User not found');
        }
    } catch (error) {
        console.error('Error updating user:', error);
        res.status(500).send('Internal Server Error');
    }
});

// Update user data
app.put('/profile', async (req, res) => {
    const userid  = req.session.userId;
    const { username, email } = req.body; // Assuming you want to update username and email
    try {
        const [result] = await db.promise().query('UPDATE users SET username = ?, email = ? WHERE id = ?', [username, email, userid]);
        if (result.affectedRows > 0) {
            res.send('User updated successfully');
        } else {
            res.status(404).send('User not found');
        }
    } catch (error) {
        console.error('Error updating user:', error);
        res.status(500).send('Internal Server Error');
    }
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
async function getFlightData(apiEndpoint,params){
    try {
        const response =await axios.get(apiEndpoint,{ params });
        return (response.data);
    } catch (error){
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
