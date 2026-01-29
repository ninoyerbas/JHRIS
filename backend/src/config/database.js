const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const dbPath = path.join(__dirname, '../../data/hris.db');

const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Error opening database:', err.message);
  } else {
    console.log('Connected to SQLite database');
    initializeDatabase();
  }
});

function initializeDatabase() {
  // Use serialize to ensure tables are created sequentially
  db.serialize(() => {
    // Users table
    db.run(`
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT NOT NULL DEFAULT 'employee',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);

    // Employees table
    db.run(`
      CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        employee_id TEXT UNIQUE NOT NULL,
        department TEXT,
        position TEXT,
        hire_date DATE,
        phone TEXT,
        address TEXT,
        status TEXT DEFAULT 'active',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
      )
    `);

    // Attendance table
    db.run(`
      CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        date DATE NOT NULL,
        clock_in DATETIME,
        clock_out DATETIME,
        status TEXT DEFAULT 'present',
        notes TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (employee_id) REFERENCES employees(id),
        UNIQUE(employee_id, date)
      )
    `);

    // Leave types table
    db.run(`
      CREATE TABLE IF NOT EXISTS leave_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT,
        max_days INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);

    // Leave balances table
    db.run(`
      CREATE TABLE IF NOT EXISTS leave_balances (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        leave_type_id INTEGER NOT NULL,
        total_days INTEGER DEFAULT 0,
        used_days INTEGER DEFAULT 0,
        remaining_days INTEGER DEFAULT 0,
        year INTEGER NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (employee_id) REFERENCES employees(id),
        FOREIGN KEY (leave_type_id) REFERENCES leave_types(id),
        UNIQUE(employee_id, leave_type_id, year)
      )
    `);

    // Leave requests table
    db.run(`
      CREATE TABLE IF NOT EXISTS leave_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        leave_type_id INTEGER NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        days INTEGER NOT NULL,
        reason TEXT,
        status TEXT DEFAULT 'pending',
        approved_by INTEGER,
        approved_at DATETIME,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (employee_id) REFERENCES employees(id),
        FOREIGN KEY (leave_type_id) REFERENCES leave_types(id),
        FOREIGN KEY (approved_by) REFERENCES users(id)
      )
    `);

    // Seed default leave types
    db.run(`
      INSERT OR IGNORE INTO leave_types (name, description, max_days) 
      VALUES 
        ('Annual Leave', 'Annual vacation leave', 15),
        ('Sick Leave', 'Medical sick leave', 10),
        ('Personal Leave', 'Personal time off', 5),
        ('Maternity Leave', 'Maternity leave', 90),
        ('Paternity Leave', 'Paternity leave', 7)
    `);
  });
}

module.exports = db;
