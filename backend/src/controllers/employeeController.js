/*
 * JHRIS - Human Resources Information System
 * Copyright (c) 2024-2026 Julio Cesar Mendez Tobar. All Rights Reserved.
 * 
 * PROPRIETARY AND CONFIDENTIAL
 * 
 * This software and associated documentation files (the "Software") are
 * the proprietary and confidential information of Julio Cesar Mendez Tobar.
 * 
 * Unauthorized copying, modification, distribution, or use of this software,
 * via any medium, is strictly prohibited without the express written permission
 * of the copyright holder.
 * 
 * Author: Julio Cesar Mendez Tobar
 */

const db = require('../config/database');

const employeeController = {
  // Create employee
  create: (req, res) => {
    const { user_id, first_name, last_name, employee_id, department, position, hire_date, phone, address } = req.body;

    if (!first_name || !last_name || !employee_id) {
      return res.status(400).json({ error: 'First name, last name, and employee ID are required' });
    }

    const query = `
      INSERT INTO employees (user_id, first_name, last_name, employee_id, department, position, hire_date, phone, address)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `;
    
    db.run(query, [user_id, first_name, last_name, employee_id, department, position, hire_date, phone, address], function(err) {
      if (err) {
        return res.status(400).json({ error: 'Employee ID already exists or invalid data' });
      }

      res.status(201).json({
        message: 'Employee created successfully',
        employeeId: this.lastID
      });
    });
  },

  // Get all employees
  getAll: (req, res) => {
    const { status, department } = req.query;
    let query = 'SELECT * FROM employees WHERE 1=1';
    const params = [];

    if (status) {
      query += ' AND status = ?';
      params.push(status);
    }

    if (department) {
      query += ' AND department = ?';
      params.push(department);
    }

    query += ' ORDER BY last_name, first_name';

    db.all(query, params, (err, employees) => {
      if (err) {
        return res.status(500).json({ error: 'Error fetching employees' });
      }
      res.json(employees);
    });
  },

  // Get employee by ID
  getById: (req, res) => {
    const query = 'SELECT * FROM employees WHERE id = ?';
    db.get(query, [req.params.id], (err, employee) => {
      if (err || !employee) {
        return res.status(404).json({ error: 'Employee not found' });
      }
      res.json(employee);
    });
  },

  // Update employee
  update: (req, res) => {
    const { first_name, last_name, department, position, phone, address, status } = req.body;
    
    const query = `
      UPDATE employees 
      SET first_name = ?, last_name = ?, department = ?, position = ?, phone = ?, address = ?, status = ?, updated_at = CURRENT_TIMESTAMP
      WHERE id = ?
    `;

    db.run(query, [first_name, last_name, department, position, phone, address, status, req.params.id], function(err) {
      if (err) {
        return res.status(400).json({ error: 'Error updating employee' });
      }

      if (this.changes === 0) {
        return res.status(404).json({ error: 'Employee not found' });
      }

      res.json({ message: 'Employee updated successfully' });
    });
  },

  // Delete employee (soft delete)
  delete: (req, res) => {
    const query = 'UPDATE employees SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?';
    db.run(query, ['inactive', req.params.id], function(err) {
      if (err) {
        return res.status(400).json({ error: 'Error deleting employee' });
      }

      if (this.changes === 0) {
        return res.status(404).json({ error: 'Employee not found' });
      }

      res.json({ message: 'Employee deleted successfully' });
    });
  }
};

module.exports = employeeController;
