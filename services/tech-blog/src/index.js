const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const winston = require('winston');
require('dotenv').config();

const postsRouter = require('./routes/posts');
const categoriesRouter = require('./routes/categories');
const authRouter = require('./routes/auth');
const tagsRouter = require('./routes/tags');

// Initialize logger
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple()
  }));
}

const app = express();

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());

// Routes
app.use('/api/posts', postsRouter);
app.use('/api/categories', categoriesRouter);
app.use('/api/auth', authRouter);
app.use('/api/tags', tagsRouter);

// Error handling middleware
app.use((err, req, res, next) => {
  logger.error(err.stack);
  res.status(500).send('Something broke!');
});

// Database connection
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/tech-blog';
const MONGODB_OPTIONS = {
  useNewUrlParser: true,
  useUnifiedTopology: true,
  serverSelectionTimeoutMS: 5000,
  socketTimeoutMS: 45000,
  connectTimeoutMS: 10000,
  retryWrites: true,
  w: 'majority'
};

mongoose.connect(MONGODB_URI, MONGODB_OPTIONS)
  .then(() => {
    logger.info('Successfully connected to MongoDB');
  })
  .catch((err) => {
    logger.error('MongoDB connection error:', {
      error: err.message,
      stack: err.stack,
      code: err.code
    });
    process.exit(1); // Exit if we can't connect to the database
  });

// Graceful shutdown
process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Closing MongoDB connection...');
  mongoose.connection.close()
    .then(() => {
      logger.info('MongoDB connection closed');
      process.exit(0);
    })
    .catch((err) => {
      logger.error('Error closing MongoDB connection:', err);
      process.exit(1);
    });
});

// Start server
const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || '0.0.0.0';

const server = app.listen(PORT, HOST, () => {
  logger.info(`Server is running on http://${HOST}:${PORT}`);
});

// Handle server errors
server.on('error', (err) => {
  logger.error('Server error:', {
    error: err.message,
    stack: err.stack,
    code: err.code
  });
  
  if (err.code === 'EADDRINUSE') {
    logger.error(`Port ${PORT} is already in use`);
    process.exit(1);
  }
}); 