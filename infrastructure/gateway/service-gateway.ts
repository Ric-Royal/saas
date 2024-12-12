import express from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';
import { healthCheck } from './health';
import { rateLimit } from 'express-rate-limit';

// Utility function to generate correlation ID
function generateCorrelationId(): string {
  return `${Date.now()}-${Math.random().toString(36).substring(2, 15)}`;
}

const app = express();

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});

app.use(limiter);

// Health check endpoint
app.get('/health', healthCheck);

// Service routes with health checks
const services = [
  {
    path: '/public-participation',
    target: 'http://public-participation:8000',
    healthEndpoint: '/health'
  },
  {
    path: '/civilbot',
    target: 'http://civilbot:8001',
    healthEndpoint: '/health'
  },
  {
    path: '/billbot',
    target: 'http://billbot:8002',
    healthEndpoint: '/health'
  },
  {
    path: '/agri-insights',
    target: 'http://agri-insights:8003',
    healthEndpoint: '/health'
  },
  {
    path: '/tech-blog',
    target: 'http://tech-blog:3004',
    healthEndpoint: '/health'
  }
];

// Set up proxy routes
services.forEach(service => {
  app.use(service.path, createProxyMiddleware({
    target: service.target,
    changeOrigin: true,
    pathRewrite: {
      [`^${service.path}`]: ''
    },
    onProxyReq: (proxyReq, req, res) => {
      // Add correlation ID for request tracing
      proxyReq.setHeader('X-Correlation-ID', req.headers['x-correlation-id'] || generateCorrelationId());
    }
  }));
});

// Error handling
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal Server Error' });
});

const port = process.env.GATEWAY_PORT || 3000;
app.listen(port, () => {
  console.log(`Service Gateway listening on port ${port}`);
}); 