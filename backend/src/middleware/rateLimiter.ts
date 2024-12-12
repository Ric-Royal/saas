import rateLimit from 'express-rate-limit';
import { RequestHandler } from 'express';

// General API rate limiter
export const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  message: { error: 'Too many requests, please try again later.' },
  standardHeaders: true,
  legacyHeaders: false,
}) as unknown as RequestHandler;

// Stricter rate limiter for auth endpoints
export const authLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 5,
  message: { error: 'Too many login attempts, please try again later.' },
  standardHeaders: true,
  legacyHeaders: false,
}) as unknown as RequestHandler;

// Rate limiter for email sending
export const emailLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 3,
  message: { error: 'Too many email requests, please try again later.' },
  standardHeaders: true,
  legacyHeaders: false,
}) as unknown as RequestHandler; 