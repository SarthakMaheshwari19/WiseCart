//User.js

const db = require('../index');

class User {

    static async findByEmail(email) {
        try {
          // Get user from the database
          const [rows] = await db.execute('SELECT * FROM users WHERE email = ?', [email]);
          return rows[0];
        } catch (error) {
          console.error('Error finding user by email:', error);
          throw error;
        }
        // finally{
        //   db.end();
        // }
      }

      static async create(userData) {
        try {
          // Insert new user
          const values = [userData.name, userData.email, userData.password];
          const [result] =await db.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', values);
          const [user] = await db.execute('SELECT * FROM users WHERE id = ?', [result.insertId]);
          return user[0];
        } catch (error) {
          console.error('Error creating user:', error);
          throw error;
        }
        // finally{
        //   db.end();
        // }
      }

}  

module.exports = User;