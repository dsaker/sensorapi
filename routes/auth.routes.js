let express = require('express')
let authCtrl = require('../controllers/auth.controller')

const router = express.Router()

router.route('/auth/signin')
  .post(authCtrl.signin)
router.route('/auth/signout')
  .get(authCtrl.signout)

module.exports = router;