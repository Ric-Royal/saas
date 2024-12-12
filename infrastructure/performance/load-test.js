import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up to 100 users
    { duration: '5m', target: 100 }, // Stay at 100 users
    { duration: '2m', target: 200 }, // Ramp up to 200 users
    { duration: '5m', target: 200 }, // Stay at 200 users
    { duration: '2m', target: 0 },   // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests should be below 500ms
    http_req_failed: ['rate<0.01'],   // Less than 1% of requests should fail
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';

export default function () {
  // Test homepage
  const homeRes = http.get(`${BASE_URL}/`);
  check(homeRes, {
    'homepage status is 200': (r) => r.status === 200,
    'homepage loads under 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);

  // Test blog posts listing
  const postsRes = http.get(`${BASE_URL}/posts`);
  check(postsRes, {
    'posts page status is 200': (r) => r.status === 200,
    'posts page loads under 800ms': (r) => r.timings.duration < 800,
  });

  sleep(1);

  // Test API endpoints
  const apiRes = http.get(`${BASE_URL}/api/posts`);
  check(apiRes, {
    'api status is 200': (r) => r.status === 200,
    'api responds under 200ms': (r) => r.timings.duration < 200,
  });

  sleep(1);
} 