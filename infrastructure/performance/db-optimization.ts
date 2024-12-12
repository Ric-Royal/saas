import { Pool } from 'pg';
import { createClient } from 'redis';

interface QueryAnalysis {
  query: string;
  avgTime: number;
  calls: number;
  suggestions: string[];
}

export class DatabaseOptimizer {
  private pool: Pool;
  private redis: ReturnType<typeof createClient>;

  constructor(dbConfig: any, redisUrl: string) {
    // Configure connection pool
    this.pool = new Pool({
      ...dbConfig,
      max: 20, // Maximum pool size
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    });

    // Configure Redis client for query caching
    this.redis = createClient({ url: redisUrl });
  }

  // Create optimized indexes
  async createIndexes(): Promise<void> {
    const indexes = [
      // Posts table indexes
      'CREATE INDEX IF NOT EXISTS idx_posts_author ON posts(author_id)',
      'CREATE INDEX IF NOT EXISTS idx_posts_created ON posts(created_at DESC)',
      'CREATE INDEX IF NOT EXISTS idx_posts_status ON posts(status)',
      'CREATE INDEX IF NOT EXISTS idx_posts_tags ON posts USING GIN(tags)',
      
      // Comments table indexes
      'CREATE INDEX IF NOT EXISTS idx_comments_post ON comments(post_id)',
      'CREATE INDEX IF NOT EXISTS idx_comments_author ON comments(author_id)',
      
      // Users table indexes
      'CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)',
      'CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)',
    ];

    for (const index of indexes) {
      await this.pool.query(index);
    }
  }

  // Query optimization wrapper
  async optimizeQuery<T>(
    key: string,
    query: string,
    params: any[] = [],
    ttl: number = 60
  ): Promise<T[]> {
    // Try cache first
    const cached = await this.redis.get(key);
    if (cached) {
      return JSON.parse(cached);
    }

    // Execute query with explain analyze
    const explain = await this.pool.query(`EXPLAIN ANALYZE ${query}`, params);
    console.log('Query plan:', explain.rows);

    // Execute actual query
    const result = await this.pool.query(query, params);
    
    // Cache result
    await this.redis.setEx(key, ttl, JSON.stringify(result.rows));
    
    return result.rows;
  }

  // Connection pool management
  async healthCheck(): Promise<boolean> {
    try {
      const client = await this.pool.connect();
      client.release();
      return true;
    } catch (error) {
      return false;
    }
  }

  // Query optimization suggestions
  async analyzeQueries(): Promise<QueryAnalysis[]> {
    const slowQueries = await this.pool.query(`
      SELECT query, calls, total_time, rows, mean_time
      FROM pg_stat_statements
      ORDER BY mean_time DESC
      LIMIT 10;
    `);

    return slowQueries.rows.map(q => ({
      query: q.query,
      avgTime: q.mean_time,
      calls: q.calls,
      suggestions: this.generateOptimizationSuggestions(q),
    }));
  }

  private generateOptimizationSuggestions(query: any): string[] {
    const suggestions: string[] = [];
    
    if (query.mean_time > 1000) {
      suggestions.push('Consider adding indexes for frequently used columns');
    }
    
    if (query.rows > 1000) {
      suggestions.push('Implement pagination for large result sets');
    }
    
    if (query.calls > 1000) {
      suggestions.push('Consider caching frequently accessed data');
    }
    
    return suggestions;
  }

  // Cleanup
  async close(): Promise<void> {
    await this.pool.end();
    await this.redis.quit();
  }
} 