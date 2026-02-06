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

const attendanceController = {
  // Clock in
  clockIn: (req, res) => {
    const { employee_id } = req.body;
    const date = new Date().toISOString().split('T')[0];
    const clock_in = new Date().toISOString();

    const query = `
      INSERT INTO attendance (employee_id, date, clock_in, status)
      VALUES (?, ?, ?, 'present')
    `;

    db.run(query, [employee_id, date, clock_in], function(err) {
      if (err) {
        return res.status(400).json({ error: 'Already clocked in today or invalid data' });
      }

      res.status(201).json({
        message: 'Clocked in successfully',
        attendanceId: this.lastID,
        clockIn: clock_in
      });
    });
  },

  // Clock out
  clockOut: (req, res) => {
    const { employee_id } = req.body;
    const date = new Date().toISOString().split('T')[0];
    const clock_out = new Date().toISOString();

    const query = `
      UPDATE attendance 
      SET clock_out = ?, updated_at = CURRENT_TIMESTAMP
      WHERE employee_id = ? AND date = ? AND clock_out IS NULL
    `;

    db.run(query, [clock_out, employee_id, date], function(err) {
      if (err) {
        return res.status(400).json({ error: 'Error clocking out' });
      }

      if (this.changes === 0) {
        return res.status(404).json({ error: 'No active clock-in found for today' });
      }

      res.json({
        message: 'Clocked out successfully',
        clockOut: clock_out
      });
    });
  },

  // Mark attendance
  markAttendance: (req, res) => {
    const { employee_id, date, status, notes } = req.body;

    if (!employee_id || !date || !status) {
      return res.status(400).json({ error: 'Employee ID, date, and status are required' });
    }

    const query = `
      INSERT INTO attendance (employee_id, date, status, notes)
      VALUES (?, ?, ?, ?)
    `;

    db.run(query, [employee_id, date, status, notes], function(err) {
      if (err) {
        return res.status(400).json({ error: 'Attendance already marked for this date or invalid data' });
      }

      res.status(201).json({
        message: 'Attendance marked successfully',
        attendanceId: this.lastID
      });
    });
  },

  // Get attendance by employee
  getByEmployee: (req, res) => {
    const { employee_id } = req.params;
    const { start_date, end_date } = req.query;

    let query = 'SELECT * FROM attendance WHERE employee_id = ?';
    const params = [employee_id];

    if (start_date && end_date) {
      query += ' AND date BETWEEN ? AND ?';
      params.push(start_date, end_date);
    }

    query += ' ORDER BY date DESC';

    db.all(query, params, (err, attendance) => {
      if (err) {
        return res.status(500).json({ error: 'Error fetching attendance' });
      }
      res.json(attendance);
    });
  },

  // Get all attendance records
  getAll: (req, res) => {
    const { date, status } = req.query;
    let query = `
      SELECT a.*, e.first_name, e.last_name, e.employee_id as emp_id, e.department
      FROM attendance a
      JOIN employees e ON a.employee_id = e.id
      WHERE 1=1
    `;
    const params = [];

    if (date) {
      query += ' AND a.date = ?';
      params.push(date);
    }

    if (status) {
      query += ' AND a.status = ?';
      params.push(status);
    }

    query += ' ORDER BY a.date DESC, e.last_name, e.first_name';

    db.all(query, params, (err, attendance) => {
      if (err) {
        return res.status(500).json({ error: 'Error fetching attendance' });
      }
      res.json(attendance);
    });
  },

  // Update attendance
  update: (req, res) => {
    const { status, notes } = req.body;
    
    const query = `
      UPDATE attendance 
      SET status = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
      WHERE id = ?
    `;

    db.run(query, [status, notes, req.params.id], function(err) {
      if (err) {
        return res.status(400).json({ error: 'Error updating attendance' });
      }

      if (this.changes === 0) {
        return res.status(404).json({ error: 'Attendance record not found' });
      }

      res.json({ message: 'Attendance updated successfully' });
    });
  }
};

module.exports = attendanceController;
