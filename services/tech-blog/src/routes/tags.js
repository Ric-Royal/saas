const express = require('express');
const router = express.Router();
const Tag = require('../models/Tag');
const { auth, authorize } = require('../middleware/auth');

// Get all tags (public)
router.get('/', async (req, res) => {
  try {
    const tags = await Tag.find({ isActive: true })
      .sort({ name: 1 });
    res.json(tags);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get single tag by slug (public)
router.get('/:slug', async (req, res) => {
  try {
    const tag = await Tag.findOne({
      slug: req.params.slug,
      isActive: true
    }).populate({
      path: 'posts',
      select: 'title slug createdAt',
      match: { status: 'published' },
      options: { sort: { createdAt: -1 } }
    });

    if (!tag) {
      return res.status(404).json({ error: 'Tag not found' });
    }

    res.json(tag);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Create new tag (admin only)
router.post('/', auth, authorize('admin'), async (req, res) => {
  try {
    const tag = new Tag(req.body);
    await tag.save();
    res.status(201).json(tag);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Update tag (admin only)
router.patch('/:id', auth, authorize('admin'), async (req, res) => {
  try {
    const tag = await Tag.findById(req.params.id);
    if (!tag) {
      return res.status(404).json({ error: 'Tag not found' });
    }

    Object.assign(tag, req.body);
    await tag.save();
    res.json(tag);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Delete tag (admin only)
router.delete('/:id', auth, authorize('admin'), async (req, res) => {
  try {
    const tag = await Tag.findById(req.params.id);
    if (!tag) {
      return res.status(404).json({ error: 'Tag not found' });
    }

    // Instead of deleting, mark as inactive
    tag.isActive = false;
    await tag.save();
    res.json({ message: 'Tag deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get popular tags (public)
router.get('/popular/all', async (req, res) => {
  try {
    const tags = await Tag.aggregate([
      { $match: { isActive: true } },
      {
        $lookup: {
          from: 'posts',
          localField: '_id',
          foreignField: 'tags',
          as: 'posts'
        }
      },
      {
        $project: {
          name: 1,
          slug: 1,
          color: 1,
          postCount: { $size: '$posts' }
        }
      },
      { $sort: { postCount: -1 } },
      { $limit: 10 }
    ]);

    res.json(tags);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router; 