import express from 'express';
import { Post } from '../models/post';
import { sendSuccess, sendError } from '../utils/apiResponse';
import { io } from '../app';
import { auth, adminAuth } from '../middleware/auth';

const router = express.Router();

// Public routes
router.get('/', async (req, res) => {
  try {
    const posts = await Post.find().sort({ createdAt: -1 });
    return sendSuccess(res, posts);
  } catch (error: any) {
    return sendError(res, error.message);
  }
});

router.get('/:id', async (req, res) => {
  try {
    const post = await Post.findById(req.params.id);
    if (!post) {
      return sendError(res, 'Post not found', 404);
    }
    return sendSuccess(res, post);
  } catch (error: any) {
    return sendError(res, error.message);
  }
});

// Protected routes
router.post('/', auth, async (req: any, res) => {
  try {
    const post = await Post.create({
      ...req.body,
      author: req.user._id
    });
    io.emit('newPost', post);
    return sendSuccess(res, post, 201);
  } catch (error: any) {
    return sendError(res, error.message, 400);
  }
});

router.put('/:id', auth, async (req: any, res) => {
  try {
    const post = await Post.findOne({ _id: req.params.id, author: req.user._id });
    if (!post) {
      return sendError(res, 'Post not found or unauthorized', 404);
    }
    
    Object.assign(post, req.body);
    await post.save();
    
    io.to(`post-${req.params.id}`).emit('postUpdate', post);
    return sendSuccess(res, post);
  } catch (error: any) {
    return sendError(res, error.message);
  }
});

router.delete('/:id', auth, async (req: any, res) => {
  try {
    const post = await Post.findOneAndDelete({ 
      _id: req.params.id,
      author: req.user._id
    });
    
    if (!post) {
      return sendError(res, 'Post not found or unauthorized', 404);
    }
    
    io.to(`post-${req.params.id}`).emit('postDelete', { id: req.params.id });
    return sendSuccess(res, null, 204);
  } catch (error: any) {
    return sendError(res, error.message);
  }
});

// Admin routes
router.delete('/:id/admin', adminAuth, async (req, res) => {
  try {
    const post = await Post.findByIdAndDelete(req.params.id);
    if (!post) {
      return sendError(res, 'Post not found', 404);
    }
    io.to(`post-${req.params.id}`).emit('postDelete', { id: req.params.id });
    return sendSuccess(res, null, 204);
  } catch (error: any) {
    return sendError(res, error.message);
  }
});

export default router; 