const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const db = require('../config/database');

const authController = {
  // Register new user
  register: async (req, res) => {
    const { username, password, email, role = 'employee' } = req.body;

    if (!username || !password || !email) {
      return res.status(400).json({ error: 'Username, password, and email are required' });
    }

    try {
      const hash = await bcrypt.hash(password, 8);
      
      const query = 'INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)';
      db.run(query, [username, hash, email, role], function(err) {
        if (err) {
          return res.status(400).json({ error: 'Username or email already exists' });
        }

        res.status(201).json({
          message: 'User registered successfully',
          userId: this.lastID
        });
      });
    } catch (error) {
      return res.status(500).json({ error: 'Error hashing password' });
    }
  },

  // Login
  login: (req, res) => {
    const { username, password } = req.body;

    if (!username || !password) {
      return res.status(400).json({ error: 'Username and password are required' });
    }

    const query = 'SELECT * FROM users WHERE username = ?';
    db.get(query, [username], (err, user) => {
      if (err || !user) {
        return res.status(401).json({ error: 'Invalid credentials' });
      }

      bcrypt.compare(password, user.password, (err, isMatch) => {
        if (err || !isMatch) {
          return res.status(401).json({ error: 'Invalid credentials' });
        }

        const token = jwt.sign(
          { id: user.id, username: user.username, role: user.role },
          process.env.JWT_SECRET,
          { expiresIn: '24h' }
        );

        res.json({
          message: 'Login successful',
          token,
          user: {
            id: user.id,
            username: user.username,
            email: user.email,
            role: user.role
          }
        });
      });
    });
  },

  // Get current user
  getCurrentUser: (req, res) => {
    const query = 'SELECT id, username, email, role, created_at FROM users WHERE id = ?';
    db.get(query, [req.user.id], (err, user) => {
      if (err || !user) {
        return res.status(404).json({ error: 'User not found' });
      }
      res.json(user);
    });
  }
};

module.exports = authController;
