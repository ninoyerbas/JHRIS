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
