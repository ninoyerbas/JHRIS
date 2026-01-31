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
