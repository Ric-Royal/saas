import request from 'supertest';
import { app } from '../../app';
import { Post } from '@models/post';
import mongoose from 'mongoose';

describe('Post API Integration Tests', () => {
  const validPost = {
    title: 'Test Post',
    content: 'Test Content',
    author: 'Test Author',
    tags: ['test', 'integration'],
  };

  describe('POST /api/posts', () => {
    it('should create a new post with valid data', async () => {
      const response = await request(app)
        .post('/api/posts')
        .send(validPost)
        .expect(201);

      expect(response.body.title).toBe(validPost.title);
      expect(response.body.content).toBe(validPost.content);
      
      const post = await Post.findById(response.body._id);
      expect(post).not.toBeNull();
    });

    it('should return 400 with invalid data', async () => {
      await request(app)
        .post('/api/posts')
        .send({})
        .expect(400);
    });
  });

  describe('GET /api/posts', () => {
    it('should return all posts', async () => {
      await Post.create(validPost);
      await Post.create({
        ...validPost,
        title: 'Second Post',
      });

      const response = await request(app)
        .get('/api/posts')
        .expect(200);

      expect(response.body.length).toBe(2);
    });
  });

  describe('GET /api/posts/:id', () => {
    it('should return a post by id', async () => {
      const post = await Post.create(validPost);

      const response = await request(app)
        .get(`/api/posts/${post._id}`)
        .expect(200);

      expect(response.body.title).toBe(validPost.title);
    });

    it('should return 404 for non-existent post', async () => {
      const fakeId = new mongoose.Types.ObjectId();
      await request(app)
        .get(`/api/posts/${fakeId}`)
        .expect(404);
    });
  });

  describe('PUT /api/posts/:id', () => {
    it('should update a post', async () => {
      const post = await Post.create(validPost);
      const updatedData = {
        title: 'Updated Title',
        content: 'Updated Content',
      };

      const response = await request(app)
        .put(`/api/posts/${post._id}`)
        .send(updatedData)
        .expect(200);

      expect(response.body.title).toBe(updatedData.title);
      expect(response.body.content).toBe(updatedData.content);
    });
  });

  describe('DELETE /api/posts/:id', () => {
    it('should delete a post', async () => {
      const post = await Post.create(validPost);

      await request(app)
        .delete(`/api/posts/${post._id}`)
        .expect(204);

      const deletedPost = await Post.findById(post._id);
      expect(deletedPost).toBeNull();
    });
  });
}); 