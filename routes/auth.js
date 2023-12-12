//auth.js


const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
//nnn
const {db}  = require('../index');
const User = require('../models/user');


router.post('/register', async (req, res) => {
    console.log(req.body)
try{
  const hashedPassword = await bcrypt.hash(req.body.password, 8);

  // Create new user
  const newUser = await User.create({
    name: req.body.name,
    email: req.body.email,
    password: hashedPassword 
  });

  // Set session and redirect
  req.session.userId = newUser.id;
  req.session.save();
  res.redirect('/');
}catch (error) {console.error('Error registering user:', error);
res.render('auth', { registerError: 'Registration failed. Please try again.' });
}
});

router.post('/login', async (req, res) => {
try{
  const user = await User.findByEmail(req.body.email);

  // Validate password
  const validPassword = await bcrypt.compare(req.body.password, user.password);

  if (validPassword) {
    // Successfully logged in
    req.session.userId = user.id; 
    req.session.save();
    return res.redirect('/'); 
  } else {
    res.render('auth', { loginError: 'Incorrect username or password.' });
    // res.redirect('/auth');
    

  }
}catch(error){console.error('Error logging in:', error);
 res.render('auth', { loginError: 'User is not registered. Please try again after registering.' });
// return res.redirect('/auth');
}

});

module.exports = router;