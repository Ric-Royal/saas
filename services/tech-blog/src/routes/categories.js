const express = require('express');
const router = express.Router();
const Category = require('../models/Category');
const { auth, authorize } = require('../middleware/auth');

// Get all categories (public)
router.get('/', async (req, res) => {
  try {
    const categories = await Category.find({ isActive: true })
      .populate('parent', 'name slug')
      .sort({ name: 1 });
    res.json(categories);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get single category by slug (public)
router.get('/:slug', async (req, res) => {
  try {
    const category = await Category.findOne({
      slug: req.params.slug,
      isActive: true
    }).populate('parent', 'name slug');

    if (!category) {
      return res.status(404).json({ error: 'Category not found' });
    }

    res.json(category);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Create new category (admin only)
router.post('/', auth, authorize('admin'), async (req, res) => {
  try {
    const category = new Category(req.body);
    await category.save();
    res.status(201).json(category);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Update category (admin only)
router.patch('/:id', auth, authorize('admin'), async (req, res) => {
  try {
    const category = await Category.findById(req.params.id);
    if (!category) {
      return res.status(404).json({ error: 'Category not found' });
    }

    Object.assign(category, req.body);
    await category.save();
    res.json(category);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Delete category (admin only)
router.delete('/:id', auth, authorize('admin'), async (req, res) => {
  try {
    const category = await Category.findById(req.params.id);
    if (!category) {
      return res.status(404).json({ error: 'Category not found' });
    }

    // Instead of deleting, mark as inactive
    category.isActive = false;
    await category.save();
    res.json({ message: 'Category deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get category hierarchy (public)
router.get('/hierarchy/all', async (req, res) => {
  try {
    const categories = await Category.find({ isActive: true, parent: null })
      .populate({
        path: 'posts',
        select: 'title slug',
        match: { status: 'published' }
      });

    res.json(categories);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router; 