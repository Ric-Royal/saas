import axios from 'axios';
import { Request, Response } from 'express';

interface ServiceHealth {
  service: string;
  status: 'healthy' | 'unhealthy';
  latency: number;
  lastChecked: string;
}

const services = [
  {
    name: 'public-participation',
    url: 'http://public-participation:8000/health'
  },
  {
    name: 'civilbot',
    url: 'http://civilbot:8001/health'
  },
  {
    name: 'billbot',
    url: 'http://billbot:8002/health'
  },
  {
    name: 'agri-insights',
    url: 'http://agri-insights:8003/health'
  },
  {
    name: 'tech-blog',
    url: 'http://tech-blog:3004/health'
  }
];

let healthCache: { [key: string]: ServiceHealth } = {};

// Update health status every 30 seconds
setInterval(updateHealthStatus, 30000);

async function updateHealthStatus() {
  for (const service of services) {
    try {
      const startTime = Date.now();
      await axios.get(service.url, { timeout: 5000 });
      const latency = Date.now() - startTime;

      healthCache[service.name] = {
        service: service.name,
        status: 'healthy',
        latency,
        lastChecked: new Date().toISOString()
      };
    } catch (error) {
      healthCache[service.name] = {
        service: service.name,
        status: 'unhealthy',
        latency: -1,
        lastChecked: new Date().toISOString()
      };
    }
  }
}

export async function healthCheck(req: Request, res: Response) {
  const healthStatus = {
    gateway: {
      status: 'healthy',
      timestamp: new Date().toISOString()
    },
    services: Object.values(healthCache)
  };

  const isHealthy = Object.values(healthCache).every(
    service => service.status === 'healthy'
  );

  res.status(isHealthy ? 200 : 503).json(healthStatus);
} 