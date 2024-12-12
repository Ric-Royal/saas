import dotenv from 'dotenv';

dotenv.config();

export const config = {
  port: process.env.GATEWAY_PORT || 3000,
  
  // Service endpoints
  services: {
    publicParticipation: {
      url: process.env.PUBLIC_PARTICIPATION_URL || 'http://public-participation:8000',
      healthEndpoint: '/health'
    },
    civilBot: {
      url: process.env.CIVILBOT_URL || 'http://civilbot:8001',
      healthEndpoint: '/health'
    },
    billBot: {
      url: process.env.BILLBOT_URL || 'http://billbot:8002',
      healthEndpoint: '/health'
    },
    agriInsights: {
      url: process.env.AGRI_INSIGHTS_URL || 'http://agri-insights:8003',
      healthEndpoint: '/health'
    },
    techBlog: {
      url: process.env.TECH_BLOG_URL || 'http://tech-blog:3004',
      healthEndpoint: '/health'
    }
  },

  // Rate limiting
  rateLimit: {
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS || '100')
  },

  // Health check
  healthCheck: {
    interval: parseInt(process.env.HEALTH_CHECK_INTERVAL || '30000'), // 30 seconds
    timeout: parseInt(process.env.HEALTH_CHECK_TIMEOUT || '5000') // 5 seconds
  },

  // Cors
  cors: {
    origin: process.env.CORS_ORIGIN || '*',
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization']
  },

  // Logging
  logging: {
    level: process.env.LOG_LEVEL || 'info',
    format: process.env.LOG_FORMAT || 'json'
  }
}; 