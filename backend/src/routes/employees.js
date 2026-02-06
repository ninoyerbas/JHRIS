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
const employeeController = require('../controllers/employeeController');
const { authMiddleware, roleMiddleware } = require('../middleware/auth');

router.use(authMiddleware);

router.post('/', roleMiddleware('admin', 'hr'), employeeController.create);
router.get('/', employeeController.getAll);
router.get('/:id', employeeController.getById);
router.put('/:id', roleMiddleware('admin', 'hr'), employeeController.update);
router.delete('/:id', roleMiddleware('admin', 'hr'), employeeController.delete);

module.exports = router;
