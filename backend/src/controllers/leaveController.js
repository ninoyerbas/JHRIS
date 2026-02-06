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

const leaveController = {
  // Get all leave types
  getLeaveTypes: (req, res) => {
    const query = 'SELECT * FROM leave_types ORDER BY name';
    db.all(query, [], (err, types) => {
      if (err) {
        return res.status(500).json({ error: 'Error fetching leave types' });
      }
      res.json(types);
    });
  },

  // Create leave request
  createRequest: (req, res) => {
    const { employee_id, leave_type_id, start_date, end_date, days, reason } = req.body;

    if (!employee_id || !leave_type_id || !start_date || !end_date || !days) {
      return res.status(400).json({ error: 'All fields are required' });
    }

    const query = `
      INSERT INTO leave_requests (employee_id, leave_type_id, start_date, end_date, days, reason)
      VALUES (?, ?, ?, ?, ?, ?)
    `;

    db.run(query, [employee_id, leave_type_id, start_date, end_date, days, reason], function(err) {
      if (err) {
        return res.status(400).json({ error: 'Error creating leave request' });
      }

      res.status(201).json({
        message: 'Leave request created successfully',
        requestId: this.lastID
      });
    });
  },

  // Get all leave requests
  getAllRequests: (req, res) => {
    const { status, employee_id } = req.query;
    let query = `
      SELECT lr.*, e.first_name, e.last_name, e.employee_id as emp_id, lt.name as leave_type_name
      FROM leave_requests lr
      JOIN employees e ON lr.employee_id = e.id
      JOIN leave_types lt ON lr.leave_type_id = lt.id
      WHERE 1=1
    `;
    const params = [];

    if (status) {
      query += ' AND lr.status = ?';
      params.push(status);
    }

    if (employee_id) {
      query += ' AND lr.employee_id = ?';
      params.push(employee_id);
    }

    query += ' ORDER BY lr.created_at DESC';

    db.all(query, params, (err, requests) => {
      if (err) {
        return res.status(500).json({ error: 'Error fetching leave requests' });
      }
      res.json(requests);
    });
  },

  // Get leave request by ID
  getRequestById: (req, res) => {
    const query = `
      SELECT lr.*, e.first_name, e.last_name, e.employee_id as emp_id, lt.name as leave_type_name
      FROM leave_requests lr
      JOIN employees e ON lr.employee_id = e.id
      JOIN leave_types lt ON lr.leave_type_id = lt.id
      WHERE lr.id = ?
    `;

    db.get(query, [req.params.id], (err, request) => {
      if (err || !request) {
        return res.status(404).json({ error: 'Leave request not found' });
      }
      res.json(request);
    });
  },

  // Approve/Reject leave request
  updateRequestStatus: (req, res) => {
    const { status } = req.body;
    const approved_by = req.user.id;

    if (!['approved', 'rejected'].includes(status)) {
      return res.status(400).json({ error: 'Invalid status' });
    }

    const query = `
      UPDATE leave_requests 
      SET status = ?, approved_by = ?, approved_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
      WHERE id = ? AND status = 'pending'
    `;

    db.run(query, [status, approved_by, req.params.id], function(err) {
      if (err) {
        return res.status(400).json({ error: 'Error updating leave request' });
      }

      if (this.changes === 0) {
        return res.status(404).json({ error: 'Leave request not found or already processed' });
      }

      // If approved, update leave balance
      if (status === 'approved') {
        db.get('SELECT employee_id, leave_type_id, days FROM leave_requests WHERE id = ?', [req.params.id], (err, request) => {
          if (err || !request) {
            console.error('Error fetching leave request for balance update:', err);
            return;
          }
          
          // Verify employee exists before updating balance
          db.get('SELECT id FROM employees WHERE id = ?', [request.employee_id], (err, employee) => {
            if (err || !employee) {
              console.error('Employee not found for leave balance update:', request.employee_id);
              return;
            }
            
            const year = new Date().getFullYear();
            const updateBalanceQuery = `
              UPDATE leave_balances 
              SET used_days = used_days + ?, remaining_days = remaining_days - ?, updated_at = CURRENT_TIMESTAMP
              WHERE employee_id = ? AND leave_type_id = ? AND year = ?
            `;
            db.run(updateBalanceQuery, [request.days, request.days, request.employee_id, request.leave_type_id, year], (err) => {
              if (err) {
                console.error('Error updating leave balance:', err);
              }
            });
          });
        });
      }

      res.json({ message: `Leave request ${status} successfully` });
    });
  },

  // Get leave balance for an employee
  getBalance: (req, res) => {
    const { employee_id } = req.params;
    const year = req.query.year || new Date().getFullYear();

    const query = `
      SELECT lb.*, lt.name as leave_type_name, lt.description
      FROM leave_balances lb
      JOIN leave_types lt ON lb.leave_type_id = lt.id
      WHERE lb.employee_id = ? AND lb.year = ?
      ORDER BY lt.name
    `;

    db.all(query, [employee_id, year], (err, balances) => {
      if (err) {
        return res.status(500).json({ error: 'Error fetching leave balances' });
      }
      res.json(balances);
    });
  },

  // Initialize leave balance for an employee
  initializeBalance: (req, res) => {
    const { employee_id, leave_type_id, total_days, year } = req.body;

    if (!employee_id || !leave_type_id || !total_days || !year) {
      return res.status(400).json({ error: 'All fields are required' });
    }

    const query = `
      INSERT INTO leave_balances (employee_id, leave_type_id, total_days, used_days, remaining_days, year)
      VALUES (?, ?, ?, 0, ?, ?)
    `;

    db.run(query, [employee_id, leave_type_id, total_days, total_days, year], function(err) {
      if (err) {
        return res.status(400).json({ error: 'Leave balance already exists or invalid data' });
      }

      res.status(201).json({
        message: 'Leave balance initialized successfully',
        balanceId: this.lastID
      });
    });
  }
};

module.exports = leaveController;
