const express = require('express');
const router = express.Router();
const Post = require('../models/Post');
const { auth, authorize } = require('../middleware/auth');

// Get all posts (public)
router.get('/', async (req, res) => {
  try {
    const { page = 1, limit = 10, category, tag, status = 'published' } = req.query;
    const query = { status };

    if (category) query.category = category;
    if (tag) query.tags = tag;

    const posts = await Post.find(query)
      .populate('author', 'username firstName lastName avatar')
      .populate('category', 'name slug')
      .populate('tags', 'name slug')
      .sort({ createdAt: -1 })
      .limit(limit * 1)
      .skip((page - 1) * limit);

    const count = await Post.countDocuments(query);

    res.json({
      posts,
      totalPages: Math.ceil(count / limit),
      currentPage: page
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get single post by slug (public)
router.get('/:slug', async (req, res) => {
  try {
    const post = await Post.findOne({ slug: req.params.slug, status: 'published' })
      .populate('author', 'username firstName lastName avatar bio')
      .populate('category', 'name slug')
      .populate('tags', 'name slug');

    if (!post) {
      return res.status(404).json({ error: 'Post not found' });
    }

    // Increment views
    post.views += 1;
    await post.save();

    res.json(post);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Create new post (authenticated)
router.post('/', auth, authorize('admin', 'author'), async (req, res) => {
  try {
    const post = new Post({
      ...req.body,
      author: req.user._id
    });
    await post.save();
    res.status(201).json(post);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Update post (authenticated)
router.patch('/:id', auth, authorize('admin', 'author'), async (req, res) => {
  try {
    const post = await Post.findOne({
      _id: req.params.id,
      author: req.user._id
    });

    if (!post) {
      return res.status(404).json({ error: 'Post not found' });
    }

    Object.assign(post, req.body);
    await post.save();
    res.json(post);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Delete post (authenticated)
router.delete('/:id', auth, authorize('admin', 'author'), async (req, res) => {
  try {
    const post = await Post.findOneAndDelete({
      _id: req.params.id,
      author: req.user._id
    });

    if (!post) {
      return res.status(404).json({ error: 'Post not found' });
    }

    res.json({ message: 'Post deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Like post (authenticated)
router.post('/:id/like', auth, async (req, res) => {
  try {
    const post = await Post.findById(req.params.id);
    if (!post) {
      return res.status(404).json({ error: 'Post not found' });
    }

    post.likes += 1;
    await post.save();
    res.json({ likes: post.likes });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router; 