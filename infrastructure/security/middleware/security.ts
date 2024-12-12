import rateLimit from 'express-rate-limit';
import helmet from 'helmet';
import hpp from 'hpp';
import { Express } from 'express';
import Redis from 'ioredis';
import { randomBytes } from 'crypto';

const redis = new Redis({
  host: process.env.REDIS_HOST || 'rate-limiter',
  port: parseInt(process.env.REDIS_PORT || '6379'),
  password: process.env.REDIS_PASSWORD,
  tls: process.env.NODE_ENV === 'production' ? {} : undefined
});

export const configureSecurityMiddleware = (app: Express) => {
  // Enhanced security headers
  app.use(helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", "data:", "https:"],
        connectSrc: ["'self'", "https:"],
        fontSrc: ["'self'", "https:", "data:"],
        objectSrc: ["'none'"],
        mediaSrc: ["'self'"],
        frameSrc: ["'none'"],
      },
    },
    xssFilter: true,
    noSniff: true,
    referrerPolicy: { policy: 'strict-origin-when-cross-origin' },
    hsts: {
      maxAge: 31536000,
      includeSubDomains: true,
      preload: true
    },
    frameguard: {
      action: 'deny'
    }
  }));

  // Enhanced rate limiting with Redis
  const apiLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // Limit each IP to 100 requests per windowMs
    message: 'Too many requests from this IP, please try again later.',
    standardHeaders: true,
    legacyHeaders: false,
    store: {
      incr: (key: string) => Promise.resolve(redis.incr(key)),
      decr: (key: string) => Promise.resolve(redis.decr(key)),
      resetKey: (key: string) => Promise.resolve(redis.del(key)),
      prefix: 'rl:',
      init: () => Promise.resolve(),
    },
  });

  // Stricter rate limits for auth endpoints
  const authLimiter = rateLimit({
    windowMs: 60 * 60 * 1000, // 1 hour
    max: 5, // Limit each IP to 5 login attempts per hour
    message: 'Too many login attempts, please try again later.',
    standardHeaders: true,
    legacyHeaders: false,
    store: {
      incr: (key: string) => Promise.resolve(redis.incr(key)),
      decr: (key: string) => Promise.resolve(redis.decr(key)),
      resetKey: (key: string) => Promise.resolve(redis.del(key)),
      prefix: 'rl:auth:',
      init: () => Promise.resolve(),
    },
  });

  // Apply rate limiting
  app.use('/api/', apiLimiter);
  app.use('/api/auth/', authLimiter);

  // Prevent HTTP Parameter Pollution
  app.use(hpp());

  // Enhanced DDOS protection middleware
  app.use((req, res, next) => {
    const ip = req.ip;
    const key = `ddos:${ip}`;
    
    redis.multi()
      .incr(key)
      .expire(key, 1) // 1 second window
      .exec((err, results) => {
        if (err) {
          return next(err);
        }
        
        if (!results) {
          return next(new Error('Redis operation failed'));
        }
        
        const requests = results[0][1] as number;
        if (requests > 50) { // More than 50 requests per second
          return res.status(429).json({
            error: 'Too many requests - DDOS protection activated',
          });
        }
        next();
      });
  });

  // Additional security headers
  app.use((req, res, next) => {
    // Generate a unique nonce for CSP
    const nonce = randomBytes(16).toString('base64');
    res.locals.nonce = nonce;

    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('X-XSS-Protection', '1; mode=block');
    res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload');
    res.setHeader('Permissions-Policy', 'geolocation=(), microphone=(), camera=()');
    res.setHeader('Cross-Origin-Embedder-Policy', 'require-corp');
    res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
    res.setHeader('Cross-Origin-Resource-Policy', 'same-origin');
    next();
  });

  // Secure cookie settings
  app.set('trust proxy', 1);
  app.use((req, res, next) => {
    res.cookie('sessionId', '', {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      path: '/',
      maxAge: 24 * 60 * 60 * 1000 // 24 hours
    });
    next();
  });
} 