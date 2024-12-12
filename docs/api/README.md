# API Documentation

## Overview
This document provides detailed information about the available API endpoints, their usage, and examples.

## Base URL
```
Production: https://api.yourdomain.com
Development: http://localhost:3000
```

## Authentication
All API endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Authentication

#### POST /api/auth/login
Login endpoint to obtain JWT token.

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "token": "string",
  "user": {
    "id": "string",
    "email": "string",
    "name": "string"
  }
}
```

### Blog Posts

#### GET /api/posts
Retrieve all blog posts.

**Query Parameters:**
- `page` (optional): Page number for pagination
- `limit` (optional): Number of items per page
- `tag` (optional): Filter by tag

**Response:**
```json
{
  "posts": [
    {
      "id": "string",
      "title": "string",
      "content": "string",
      "author": "string",
      "createdAt": "string",
      "tags": ["string"]
    }
  ],
  "totalPages": "number",
  "currentPage": "number"
}
```

#### POST /api/posts
Create a new blog post.

**Request Body:**
```json
{
  "title": "string",
  "content": "string",
  "tags": ["string"]
}
```

### Comments

#### GET /api/posts/{postId}/comments
Get comments for a specific post.

#### POST /api/posts/{postId}/comments
Add a comment to a post.

**Request Body:**
```json
{
  "content": "string"
}
```

## Error Handling
All endpoints return standard HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

Error responses follow this format:
```json
{
  "error": {
    "message": "string",
    "code": "string"
  }
}
```

## Rate Limiting
API requests are limited to 100 requests per IP address per 15 minutes.

## CORS
CORS is enabled for all origins in development and specific origins in production. 