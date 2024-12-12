import Redis from 'ioredis';
import { promisify } from 'util';

export class CacheManager {
  private redis: Redis;
  private defaultTTL: number = 3600; // 1 hour

  constructor(redisUrl: string) {
    this.redis = new Redis(redisUrl);
  }

  // Cache strategies
  async getOrSet<T>(
    key: string,
    fetchFn: () => Promise<T>,
    ttl: number = this.defaultTTL
  ): Promise<T> {
    const cached = await this.redis.get(key);
    if (cached) {
      return JSON.parse(cached);
    }

    const data = await fetchFn();
    await this.redis.setex(key, ttl, JSON.stringify(data));
    return data;
  }

  // Sliding window rate limiter
  async checkRateLimit(key: string, limit: number, window: number): Promise<boolean> {
    const now = Date.now();
    const clearBefore = now - window * 1000;

    const multi = this.redis.multi();
    multi.zremrangebyscore(key, 0, clearBefore);
    multi.zadd(key, now, now.toString());
    multi.zcard(key);
    multi.expire(key, window);

    const result = await multi.exec();
    if (!result) return false;
    const count = result[2][1] as number;
    return count <= limit;
  }

  // Cache invalidation patterns
  async invalidatePattern(pattern: string): Promise<void> {
    const keys = await this.redis.keys(pattern);
    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
  }

  // Cache warming
  async warmCache<T>(key: string, data: T, ttl: number = this.defaultTTL): Promise<void> {
    await this.redis.setex(key, ttl, JSON.stringify(data));
  }

  // Cache strategies by content type
  async cachePageData(pageId: string, data: any, ttl: number = 300): Promise<void> {
    await this.warmCache(`page:${pageId}`, data, ttl);
  }

  async cacheApiResponse(endpoint: string, data: any, ttl: number = 60): Promise<void> {
    await this.warmCache(`api:${endpoint}`, data, ttl);
  }

  async cacheUserSession(userId: string, data: any, ttl: number = 86400): Promise<void> {
    await this.warmCache(`session:${userId}`, data, ttl);
  }

  // Cache health check
  async healthCheck(): Promise<boolean> {
    try {
      await this.redis.ping();
      return true;
    } catch (error) {
      return false;
    }
  }

  // Cleanup
  async close(): Promise<void> {
    await this.redis.quit();
  }
} 