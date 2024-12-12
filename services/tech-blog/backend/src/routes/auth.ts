import express from 'express';
import { User } from '../models/user';
import { auth } from '../middleware/auth';
import { sendSuccess, sendError } from '../utils/apiResponse';

const router = express.Router();

// Register
router.post('/register', async (req, res) => {
  try {
    const user = new User(req.body);
    await user.save();
    const token = await user.generateAuthToken();
    sendSuccess(res, { user, token }, 201);
  } catch (error: any) {
    sendError(res, error.message, 400);
  }
});

// Login
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    const user = await User.findOne({ email });

    if (!user || !(await user.comparePassword(password))) {
      throw new Error('Invalid login credentials');
    }

    const token = await user.generateAuthToken();
    sendSuccess(res, { user, token });
  } catch (error: any) {
    sendError(res, error.message, 401);
  }
});

// Get current user
router.get('/me', auth, async (req: any, res) => {
  try {
    sendSuccess(res, { user: req.user });
  } catch (error: any) {
    sendError(res, error.message);
  }
});

// Update profile
router.patch('/me', auth, async (req: any, res) => {
  const updates = Object.keys(req.body);
  const allowedUpdates = ['name', 'email', 'password', 'bio', 'avatar'];
  const isValidOperation = updates.every(update => allowedUpdates.includes(update));

  if (!isValidOperation) {
    return sendError(res, 'Invalid updates', 400);
  }

  try {
    updates.forEach(update => req.user[update] = req.body[update]);
    await req.user.save();
    sendSuccess(res, { user: req.user });
  } catch (error: any) {
    sendError(res, error.message, 400);
  }
});

// Logout
router.post('/logout', auth, async (req: any, res) => {
  try {
    sendSuccess(res, { message: 'Logged out successfully' });
  } catch (error: any) {
    sendError(res, error.message);
  }
});

export default router; 