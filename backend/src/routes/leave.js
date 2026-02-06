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

const express = require('express');
const router = express.Router();
const leaveController = require('../controllers/leaveController');
const { authMiddleware, roleMiddleware } = require('../middleware/auth');

router.use(authMiddleware);

router.get('/types', leaveController.getLeaveTypes);
router.post('/requests', leaveController.createRequest);
router.get('/requests', leaveController.getAllRequests);
router.get('/requests/:id', leaveController.getRequestById);
router.put('/requests/:id', roleMiddleware('admin', 'hr', 'manager'), leaveController.updateRequestStatus);
router.get('/balance/:employee_id', leaveController.getBalance);
router.post('/balance', roleMiddleware('admin', 'hr'), leaveController.initializeBalance);

module.exports = router;
