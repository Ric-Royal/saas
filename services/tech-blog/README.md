# Tech Blog Service

A modern, feature-rich blogging platform built with Node.js, Express, and MongoDB.

## Features

- User authentication and authorization
- Blog post management with drafts and publishing
- Category and tag organization
- Rich text editing support
- View counts and likes
- User profiles
- RESTful API

## Prerequisites

- Node.js 18 or higher
- MongoDB
- Docker (optional)

## Installation

1. Clone the repository
2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file with the following variables:
```
PORT=3004
MONGODB_URI=mongodb://mongodb:27017/tech-blog
JWT_SECRET=your_jwt_secret_key_here
NODE_ENV=development
```

## Development

Start the development server:
```bash
npm run dev
```

## Production

Build and start the production server:
```bash
npm start
```

## Docker

Build the container:
```bash
docker build -t tech-blog .
```

Run the container:
```bash
docker run -p 3004:3004 tech-blog
```

## API Endpoints

### Authentication
- POST /api/auth/register - Register new user
- POST /api/auth/login - Login user
- GET /api/auth/me - Get current user
- PATCH /api/auth/me - Update user profile

### Posts
- GET /api/posts - Get all posts
- GET /api/posts/:slug - Get single post
- POST /api/posts - Create new post
- PATCH /api/posts/:id - Update post
- DELETE /api/posts/:id - Delete post
- POST /api/posts/:id/like - Like post

### Categories
- GET /api/categories - Get all categories
- GET /api/categories/:slug - Get single category
- POST /api/categories - Create new category
- PATCH /api/categories/:id - Update category
- DELETE /api/categories/:id - Delete category
- GET /api/categories/hierarchy/all - Get category hierarchy

### Tags
- GET /api/tags - Get all tags
- GET /api/tags/:slug - Get single tag
- POST /api/tags - Create new tag
- PATCH /api/tags/:id - Update tag
- DELETE /api/tags/:id - Delete tag
- GET /api/tags/popular/all - Get popular tags

## Testing

Run tests:
```bash
npm test
```

## License

MIT 