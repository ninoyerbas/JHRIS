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

// API Configuration
const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:3001/api'
    : `${window.location.origin}/api`;
let token = localStorage.getItem('token');
let currentUser = null;

// Utility Functions
function showPage(pageId) {
    document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));
    document.getElementById(pageId).classList.add('active');
}

function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => section.classList.remove('active'));
    document.getElementById(sectionId).classList.add('active');
    
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    document.querySelector(`[data-page="${sectionId.replace('-section', '')}"]`)?.classList.add('active');
}

function showError(elementId, message) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.style.display = 'block';
    setTimeout(() => {
        element.style.display = 'none';
    }, 5000);
}

function showSuccess(elementId, message) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.className = 'success-message';
    element.style.display = 'block';
    setTimeout(() => {
        element.style.display = 'none';
        element.className = 'error-message';
    }, 3000);
}

async function apiRequest(endpoint, method = 'GET', body = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    };

    if (token) {
        options.headers['Authorization'] = `Bearer ${token}`;
    }

    if (body) {
        options.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(`${API_URL}${endpoint}`, options);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'An error occurred');
        }
        
        return data;
    } catch (error) {
        throw error;
    }
}

// Authentication
document.getElementById('login-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const data = await apiRequest('/auth/login', 'POST', { username, password });
        token = data.token;
        localStorage.setItem('token', token);
        currentUser = data.user;
        document.getElementById('user-name').textContent = data.user.username;
        showPage('dashboard-page');
        loadDashboard();
    } catch (error) {
        showError('login-error', error.message);
    }
});

document.getElementById('register-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('reg-username').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;

    try {
        await apiRequest('/auth/register', 'POST', { username, email, password });
        showSuccess('register-error', 'Registration successful! Please login.');
        setTimeout(() => {
            showPage('login-page');
        }, 2000);
    } catch (error) {
        showError('register-error', error.message);
    }
});

document.getElementById('show-register')?.addEventListener('click', (e) => {
    e.preventDefault();
    showPage('register-page');
});

document.getElementById('show-login')?.addEventListener('click', (e) => {
    e.preventDefault();
    showPage('login-page');
});

document.getElementById('logout-btn')?.addEventListener('click', () => {
    localStorage.removeItem('token');
    token = null;
    currentUser = null;
    showPage('login-page');
});

// Navigation
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const page = link.getAttribute('data-page');
        showSection(`${page}-section`);
        
        if (page === 'dashboard') loadDashboard();
        else if (page === 'employees') loadEmployees();
        else if (page === 'attendance') loadAttendance();
        else if (page === 'leave') loadLeaveRequests();
    });
});

// Dashboard Functions
async function loadDashboard() {
    try {
        const employees = await apiRequest('/employees');
        const attendance = await apiRequest('/attendance?date=' + new Date().toISOString().split('T')[0]);
        const leaveRequests = await apiRequest('/leave/requests?status=pending');

        document.getElementById('total-employees').textContent = employees.filter(e => e.status === 'active').length;
        document.getElementById('present-today').textContent = attendance.filter(a => a.status === 'present').length;
        document.getElementById('pending-leaves').textContent = leaveRequests.length;
        
        const departments = [...new Set(employees.map(e => e.department))].filter(d => d);
        document.getElementById('active-departments').textContent = departments.length;
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

// Employee Functions
async function loadEmployees() {
    try {
        const employees = await apiRequest('/employees');
        const tbody = document.querySelector('#employees-table tbody');
        tbody.innerHTML = '';

        employees.forEach(employee => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${employee.employee_id}</td>
                <td>${employee.first_name} ${employee.last_name}</td>
                <td>${employee.department || 'N/A'}</td>
                <td>${employee.position || 'N/A'}</td>
                <td><span class="status-badge status-${employee.status}">${employee.status}</span></td>
                <td class="action-buttons">
                    <button class="btn btn-primary btn-sm" onclick="viewEmployee(${employee.id})">View</button>
                    ${currentUser && ['admin', 'hr'].includes(currentUser.role) ? 
                        `<button class="btn btn-danger btn-sm" onclick="deleteEmployee(${employee.id})">Delete</button>` : ''}
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading employees:', error);
    }
}

document.getElementById('add-employee-btn')?.addEventListener('click', () => {
    showEmployeeModal();
});

function showEmployeeModal(employee = null) {
    const modal = document.createElement('div');
    modal.className = 'modal active';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h2>${employee ? 'Edit' : 'Add'} Employee</h2>
                <button class="close-modal">&times;</button>
            </div>
            <form id="employee-form">
                <div class="form-group">
                    <label>Employee ID</label>
                    <input type="text" name="employee_id" value="${employee?.employee_id || ''}" required ${employee ? 'readonly' : ''}>
                </div>
                <div class="form-group">
                    <label>First Name</label>
                    <input type="text" name="first_name" value="${employee?.first_name || ''}" required>
                </div>
                <div class="form-group">
                    <label>Last Name</label>
                    <input type="text" name="last_name" value="${employee?.last_name || ''}" required>
                </div>
                <div class="form-group">
                    <label>Department</label>
                    <input type="text" name="department" value="${employee?.department || ''}">
                </div>
                <div class="form-group">
                    <label>Position</label>
                    <input type="text" name="position" value="${employee?.position || ''}">
                </div>
                <div class="form-group">
                    <label>Phone</label>
                    <input type="tel" name="phone" value="${employee?.phone || ''}">
                </div>
                <div class="form-group">
                    <label>Address</label>
                    <input type="text" name="address" value="${employee?.address || ''}">
                </div>
                <div class="form-group">
                    <label>Hire Date</label>
                    <input type="date" name="hire_date" value="${employee?.hire_date || ''}">
                </div>
                <button type="submit" class="btn btn-primary">Save</button>
            </form>
        </div>
    `;

    document.body.appendChild(modal);

    modal.querySelector('.close-modal').addEventListener('click', () => {
        modal.remove();
    });

    modal.querySelector('#employee-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData);

        try {
            if (employee) {
                await apiRequest(`/employees/${employee.id}`, 'PUT', data);
            } else {
                await apiRequest('/employees', 'POST', data);
            }
            modal.remove();
            loadEmployees();
        } catch (error) {
            alert('Error: ' + error.message);
        }
    });
}

async function viewEmployee(id) {
    try {
        const employee = await apiRequest(`/employees/${id}`);
        showEmployeeModal(employee);
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function deleteEmployee(id) {
    if (confirm('Are you sure you want to delete this employee?')) {
        try {
            await apiRequest(`/employees/${id}`, 'DELETE');
            loadEmployees();
        } catch (error) {
            alert('Error: ' + error.message);
        }
    }
}

// Attendance Functions
async function loadAttendance() {
    const date = document.getElementById('attendance-date').value || new Date().toISOString().split('T')[0];
    
    try {
        const attendance = await apiRequest(`/attendance?date=${date}`);
        const tbody = document.querySelector('#attendance-table tbody');
        tbody.innerHTML = '';

        attendance.forEach(record => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${new Date(record.date).toLocaleDateString()}</td>
                <td>${record.first_name} ${record.last_name}</td>
                <td>${record.department || 'N/A'}</td>
                <td>${record.clock_in ? new Date(record.clock_in).toLocaleTimeString() : '-'}</td>
                <td>${record.clock_out ? new Date(record.clock_out).toLocaleTimeString() : '-'}</td>
                <td><span class="status-badge status-${record.status}">${record.status}</span></td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading attendance:', error);
    }
}

document.getElementById('filter-attendance-btn')?.addEventListener('click', () => {
    loadAttendance();
});

document.getElementById('attendance-date').value = new Date().toISOString().split('T')[0];

// Clock In/Out
document.getElementById('clock-in-btn')?.addEventListener('click', async () => {
    try {
        const employees = await apiRequest('/employees');
        const userEmployee = employees.find(e => e.user_id === currentUser?.id);
        
        if (!userEmployee) {
            alert('No employee record found for your user account');
            return;
        }

        await apiRequest('/attendance/clock-in', 'POST', { employee_id: userEmployee.id });
        alert('Clocked in successfully!');
        loadDashboard();
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

document.getElementById('clock-out-btn')?.addEventListener('click', async () => {
    try {
        const employees = await apiRequest('/employees');
        const userEmployee = employees.find(e => e.user_id === currentUser?.id);
        
        if (!userEmployee) {
            alert('No employee record found for your user account');
            return;
        }

        await apiRequest('/attendance/clock-out', 'POST', { employee_id: userEmployee.id });
        alert('Clocked out successfully!');
        loadDashboard();
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

// Leave Functions
async function loadLeaveRequests() {
    try {
        const requests = await apiRequest('/leave/requests');
        const tbody = document.querySelector('#leave-table tbody');
        tbody.innerHTML = '';

        requests.forEach(request => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${request.first_name} ${request.last_name}</td>
                <td>${request.leave_type_name}</td>
                <td>${new Date(request.start_date).toLocaleDateString()}</td>
                <td>${new Date(request.end_date).toLocaleDateString()}</td>
                <td>${request.days}</td>
                <td><span class="status-badge status-${request.status}">${request.status}</span></td>
                <td class="action-buttons">
                    ${request.status === 'pending' && currentUser && ['admin', 'hr', 'manager'].includes(currentUser.role) ? `
                        <button class="btn btn-success btn-sm" onclick="approveLeave(${request.id})">Approve</button>
                        <button class="btn btn-danger btn-sm" onclick="rejectLeave(${request.id})">Reject</button>
                    ` : '-'}
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading leave requests:', error);
    }
}

async function approveLeave(id) {
    try {
        await apiRequest(`/leave/requests/${id}`, 'PUT', { status: 'approved' });
        loadLeaveRequests();
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function rejectLeave(id) {
    try {
        await apiRequest(`/leave/requests/${id}`, 'PUT', { status: 'rejected' });
        loadLeaveRequests();
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

document.getElementById('new-leave-request-btn')?.addEventListener('click', () => {
    showLeaveRequestModal();
});

document.getElementById('request-leave-btn')?.addEventListener('click', () => {
    showLeaveRequestModal();
});

async function showLeaveRequestModal() {
    try {
        const employees = await apiRequest('/employees');
        const leaveTypes = await apiRequest('/leave/types');
        const userEmployee = employees.find(e => e.user_id === currentUser?.id);

        const modal = document.createElement('div');
        modal.className = 'modal active';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2>Request Leave</h2>
                    <button class="close-modal">&times;</button>
                </div>
                <form id="leave-request-form">
                    <div class="form-group">
                        <label>Leave Type</label>
                        <select name="leave_type_id" required>
                            ${leaveTypes.map(type => `<option value="${type.id}">${type.name}</option>`).join('')}
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Start Date</label>
                        <input type="date" name="start_date" required>
                    </div>
                    <div class="form-group">
                        <label>End Date</label>
                        <input type="date" name="end_date" required>
                    </div>
                    <div class="form-group">
                        <label>Number of Days</label>
                        <input type="number" name="days" min="1" required>
                    </div>
                    <div class="form-group">
                        <label>Reason</label>
                        <textarea name="reason" rows="3"></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Submit Request</button>
                </form>
            </div>
        `;

        document.body.appendChild(modal);

        modal.querySelector('.close-modal').addEventListener('click', () => {
            modal.remove();
        });

        modal.querySelector('#leave-request-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            data.employee_id = userEmployee.id;

            try {
                await apiRequest('/leave/requests', 'POST', data);
                modal.remove();
                alert('Leave request submitted successfully!');
                loadLeaveRequests();
                loadDashboard();
            } catch (error) {
                alert('Error: ' + error.message);
            }
        });
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// Initialize app
if (token) {
    apiRequest('/auth/me').then(user => {
        currentUser = user;
        document.getElementById('user-name').textContent = user.username;
        showPage('dashboard-page');
        loadDashboard();
    }).catch(() => {
        localStorage.removeItem('token');
        token = null;
        showPage('login-page');
    });
} else {
    showPage('login-page');
}
