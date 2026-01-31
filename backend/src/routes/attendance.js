const express = require('express');
const router = express.Router();
const attendanceController = require('../controllers/attendanceController');
const { authMiddleware, roleMiddleware } = require('../middleware/auth');

router.use(authMiddleware);

router.post('/clock-in', attendanceController.clockIn);
router.post('/clock-out', attendanceController.clockOut);
router.post('/mark', roleMiddleware('admin', 'hr', 'manager'), attendanceController.markAttendance);
router.get('/', roleMiddleware('admin', 'hr', 'manager'), attendanceController.getAll);
router.get('/employee/:employee_id', attendanceController.getByEmployee);
router.put('/:id', roleMiddleware('admin', 'hr'), attendanceController.update);

module.exports = router;
